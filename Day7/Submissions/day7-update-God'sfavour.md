# Day 7: Understanding Terraform State - Part 2
### Name: God'sfavour Braimah
### Date: 12/10/24
### Time: 4:46pm
## Overview
Day 7 of the Terraform 30-Day Challenge focused on **state isolation** using **Workspaces**. Terraform Workspaces allow you to manage multiple isolated states in a single configuration directory, ideal for managing environments such as `dev`, `prod`, and `stage`.

---

## Objectives
- Understand the concept of Terraform Workspaces.
- Learn how to create and switch between multiple environments using Workspaces.
- Isolate Terraform state for each environment.

---

## Steps

### 1. Initialize Terraform
Start by initializing your Terraform directory to prepare it for configuration:
```bash
terraform init
```
### 2. List Existing Workspaces
```
  terraform workspace list
```

### 3  Create New Workspaces
Create isolated workspaces for different environments:
```
terraform workspace new dev
terraform workspace new prod
terraform workspace new stage
```
### 4. Verify Workspaces
List all workspaces to ensure they were created successfully:
```
terraform workspace list
```
outputs

 **`default`**
 **`stage`**
 **`prod`**
 **`dev`**

### Results
Successfully created and switched between Terraform Workspaces for **`dev`** **`prod`**, and **`stage`**.
Isolated Terraform states for each environment.
