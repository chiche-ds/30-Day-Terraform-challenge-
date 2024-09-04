
# Day4: Mastering Basic Infrastructure with Terraform

### Name: Adaeze Nnamdi-Udekwe
### Task Completed: Day 8: Reusing Infrastructure with Modules
### Date: 8/28/24
### Time: 5:16pm

### Module Basics", "Inputs", and "Outputs

I was able to understand how to create reusable modules. Terraform modules are then main way to package,organise and reuse configurations within terraform. In other words, modules are terraform configurations put inside a folder. You see that root directory (folder ) you create to work on your terraform files, that's your root module,which can in turn have child modules (you can call it children modules if you want.😅)
Modules in terraform can be sourced from different locations which includes local and remote sources.

I personally got to understand that in referencing an output block in your root "main.tf" file,your value naming convention will be (module.module_name.output_name) . That isn't a real name but a description of what should be after every period sign.


