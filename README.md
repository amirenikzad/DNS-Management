# DNS Management

A simple Flask web app to manage DNS entries using MongoDB. The app allows users to register domains, search for existing entries, count total DNS entries, and perform CRUD operations.

## Main Page
This is the main page of the DNS Management, where users can input domain names and IP addresses for registration or searching.
![Screenshot 2024-09-24 162110](https://github.com/user-attachments/assets/8fa37891-ac8e-4d5e-a820-142c021d0e6a)

## Edit DNS Entry
This page is used to modify an existing DNS entry. Users can update the domain name and its IP address.
![Screenshot 2024-09-24 163146](https://github.com/user-attachments/assets/b858ef73-481a-4d2e-9bc3-18ab72ccc375)

## What you see in MongoDB
![Screenshot 2024-09-24 162225](https://github.com/user-attachments/assets/afe0c12a-4edf-4a3b-921e-d1ee0b4b8589)

## Features

- **Main Page**
  - **Route**: `/`
  - **Method**: `GET`
  - Displays a form to input domain names and IP addresses.

- **Domain Registration**
  - **Route**: `/register`
  - **Method**: `POST`
  - Registers a domain name and associates it with an IP address in a hierarchical structure within MongoDB.

- **Domain Search**
  - **Route**: `/search`
  - **Methods**: `GET`, `POST`
  - Searches for a domain and retrieves the associated IP address from MongoDB.

- **Count Total DNS Entries**
  - **Route**: `/count`
  - **Method**: `GET`
  - Counts and displays the total DNS entries in the MongoDB database.

- **CRUD Operations**
  - **Route**: `/crud`
  - **Method**: `GET`
  - Lists all DNS entries and allows editing or deleting them.

- **Add DNS Entry**
  - **Route**: `/add`
  - **Methods**: `GET`, `POST`
  - Adds a new DNS entry with a domain and IP address.

- **Edit DNS Entry**
  - **Route**: `/edit/<entry_id>`
  - **Methods**: `GET`, `POST`
  - Edits an existing DNS entry using its ID.

- **Delete DNS Entry**
  - **Route**: `/delete/<entry_id>`
  - **Method**: `POST`
  - Deletes a DNS entry by ID.

## MongoDB Structure

- Domains are stored hierarchically, with each domain level (e.g., `.com`, `example`) in separate MongoDB collections. The app uses `update_one` and `aggregate` methods for data management.

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install Flask pymongo
##Ensure MongoDB is running at mongodb://localhost:27017/

app.py: Main Flask application code.
templates/domain.html: Template for domain registration and search.
templates/crud.html: Template for DNS entry management.
templates/edit_dns.html: Template for editing DNS entries.
