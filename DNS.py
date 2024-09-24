from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, Response
from urllib.parse import quote_plus
from datetime import datetime
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_main_page():
    if request.method == 'GET':
        return render_template('./domain.html')
@app.route('/register', methods=['POST'])
def domain():
    if request.method == 'POST':
        domain_name = request.form.get('domain')
        address = request.form.get('ip')
        if "." not in domain_name:
            return render_template('./domain.html', create_result="Invalid domain name.")
        names = domain_name.split(".")
        names.reverse()
        for index, name in enumerate(names):
            db = client[str(index)]
            collection = db[name]
            if index != len(names) - 1:
                collection.update_one(
                    {
                        "child_name": (
                            names[index + 1]
                            if index + 1 <= len(names) - 1
                            else f"!{address}"
                        ),
                        "parent_name": names[index - 1] if index > 0 else "^",
                    },
                    {
                        "$set": {
                            "child_name": (
                                names[index + 1]
                                if index + 1 <= len(names) - 1
                                else f"!{address}"
                            ),
                            "parent_name": names[index - 1] if index > 0 else "^",
                        }
                    },
                    upsert=True,
                )
            else:
                collection.update_one(
                {
                    "parent_name": names[index - 1] if index > 0 else "^",
                },
                {
                    "$set": {
                        "child_name": (
                            names[index + 1]
                            if index + 1 <= len(names) - 1
                            else f"!{address}"
                        ),
                    }
                },
                upsert=True,
                )
        return render_template('./domain.html', create_result=f"Domain name {domain_name} registered successfully.")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        domain_for_search = request.form.get('search')
        if "." not in domain_for_search:
            return render_template('./domain.html', result=f"Invalid domain name.")
        names = domain_for_search.split('.')
        names.reverse()
        for index, name in enumerate(names):
            db = client[str(index)]
            collection = db[name]
            if index < len(names) - 1:
                result = collection.aggregate([
                    {
                        "$match": {
                            "child_name": names[index + 1],
                            "parent_name": names[index - 1] if index > 0 else "^"
                        }
                    },
                    {
                        "$limit": 1
                    }
                ])
            else:
                result = collection.aggregate([
                    {
                        "$match": {
                            "parent_name": names[index - 1] if index > 0 else "^"
                        }
                    },
                    {
                        "$limit": 1
                    }
                ])   
            for document in result:
                result = document
            if result == None:
                return render_template('./domain.html', result=f"No Result found for IP: {domain_for_search}.")
            if index == len(names) - 1 and result:
                if result["child_name"][0] == "!":
                    return render_template('./domain.html', result=f"IP: {domain_for_search}, Address: {result['child_name'][1:]}")

            elif index == len(names) - 1 and not result:
                return render_template('./domain.html', result=f"No Result found for IP: {domain_for_search}.")
            else:
                continue


@app.route('/count', methods=['GET'])
def count():
    total_count = 0
    for index in range(10):  # Assuming you have up to 10 collections
        db = client[str(index)]
        for collection_name in db.list_collection_names():
            collection = db[collection_name]
            print("     START")
            print("collection", collection)
            count = collection.count_documents({})
            print("count", count)
            total_count += count
    print("     count", count)
    return render_template('./domain.html', aggregate_result=f"Total registered DNS entries: {total_count}")

for index in range(10): 
        db = client[str(index)]
        for collection_name in db.list_collection_names():
            collection = db[collection_name]

@app.route('/crud', methods=['GET'])
def et_dns_entries():
    pipeline = [
    {
        "$group": {
            "_id": "$parent_name",
            "entries": {
                "$push": {
                    "ip": "$child_name",
                    "id": "$_id"
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "domain": "$_id",
            "entries": 1
        }
    },
    {
        "$unwind": "$entries"
    },
    {
        "$project": {
            "domain": 1,
            "ip": "$entries.ip",
            "id": "$entries.id"
        }
    },
    {
        "$sort": {
            "domain": 1
        }
    }
]

    result = list(collection.aggregate(pipeline))
    print("result" , result)
    print("     end")
    return render_template('crud.html', dns_entries=result)

@app.route('/add', methods=['GET', 'POST'])
def add_dns_entry():
    if request.method == 'POST':
        domain_name = request.form.get('domain')
        ip_address = request.form.get('ip')
        entry = {'domain': domain_name, 'ip': ip_address}
        collection.insert_one(entry)
        return redirect(url_for('et_dns_entries'))
    else:
        return render_template('domain.html')

@app.route('/edit/<string:entry_id>', methods=['GET', 'POST'])
def edit_dns_entry(entry_id):
    entry = collection.find_one({'_id': ObjectId(entry_id)})  # Fetch the DNS entry from the database
    print("find entry_id", entry_id)
    if request.method == 'POST':
        new_domain = request.form.get('domain')
        new_ip = request.form.get('ip')
        
        pipeline = [
            {"$match": {"_id": ObjectId(entry_id)}},
            {"$set": {"parent_name": new_domain, "child_name": new_ip}}
        ]
        result = list(collection.aggregate(pipeline))
        return redirect(url_for('et_dns_entries'))
    return render_template('edit_dns.html', entry=entry, entry_id=entry_id)

@app.route('/delete/<string:entry_id>', methods=['POST'])
def delete_dns_entry(entry_id):
    pipeline = [
        {
            "$match": {
                "_id": ObjectId(entry_id) 
            }
        },
        {
            "$project": {
                "_id": 1  
            }
        }
    ]

    result = collection.aggregate(pipeline)
    deleted_count = 0
    for doc in result:
        collection.delete_one({"_id": doc["_id"]})
        deleted_count += 1
    return redirect(url_for('et_dns_entries'))


if __name__ == '__main__':
    app.run()
