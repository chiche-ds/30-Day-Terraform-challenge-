# Day 9: Continuing Reuse of Infrastructure with Modules

## Overview

Welcome to Day 9 of the Terraform 30-Day Challenge! Today, we will build on the concepts from Day 8, continuing our work with Terraform modules. We'll delve deeper into more advanced module features such as nested modules, module versioning, and reusing modules across multiple environments. By the end of the day, you’ll have a solid understanding of how to manage more complex infrastructure setups using reusable modules.

## Tasks for Today

### 1. **Reading**
   - **Chapter**: Continue with Chapter 4 (Pages 115-139)
     - Sections: "Moudel Gotchas ", "Module Versioning".
   - **Goal**: Learn more advanced concepts of working with modules, including how to manage versioning, use nested modules, and reuse modules in different environments.

### 2. **Videos**
   - **Udemy**: Watch the following videos:
     - Video 38: "Terraform module - Scope"
     - Video 39: "Terraform module -  Public registry "
     - Video 40: "Terraform module - Versioning"
   - **Goal**: Deepen your understanding of Terraform modules and learn how to manage modules across different versions and environments.

### 3. **Activity**
   - **Enhance Your Module**: Add advanced features to your module from Day 9, such as supporting multiple environments (dev, staging, production) or enabling versioning for the module.
   - **Deploy Across Environments**: Use your enhanced module to deploy infrastructure across multiple environments (e.g., dev, staging, production).

### 4. **Bonus Hands-On Project**
   - **Goal**: Refactor your Terraform module to support versioning. Use multiple versions of the same module in different environments. Then, create a separate project that consumes the versioned modules for deployment.
   - **Steps**: Refactor your module to enable versioning and support different configurations for dev, staging, and production environments. Test the deployment of these different module versions across each environment. Share both the module and the consuming project on GitHub with instructions for reuse.
   - **Deliverables**: Include code examples demonstrating how versioning is handled and share the updated module repository on GitHub.

### 5. **Blog Post**
   - **Title**: "Advanced Terraform Module Usage: Versioning, Nesting, and Reuse Across Environments"

### 6. **Social Media Post**
   - **Text**: "🔄 Expanded my knowledge of reusable Terraform modules by adding versioning and deploying across environments! #HUG #hashicorp #HUGYDE @chiche #IaC"

## How to Submit Your Work
The submissions folder has been updated with a [submissionTemplate](https://github.com/chiche-ds/30-Day-Terraform-challenge-/blob/main/Day9/Submissions/submissionTemplate.md) file. Use this file as a template to create your daily update.md file in the submission folder 

### 1. **Create the `day9-update-your-github-username.md` File**
   - Include your Terraform code and any architecture diagrams in the markdown file.
   - Document your enhanced module, including details about versioning, environment configuration, and deployment strategies.
   - Save the file in your `day9-advanced-modules` branch.

### 2. **Commit Your Changes**
   - Stage and commit your changes with a message like:
     ```bash
     git add day9-update-your-github-username.md
     git commit -m "Completed Day 9 task on advanced Terraform modules"
     ```

### 3. **Create a Pull Request**
   - Push your changes to your GitHub repository:
     ```bash
     git push origin day9-advanced-modules
     ```
   - Create a pull request using the provided template and include any additional comments if necessary.

## Checklist

- [ ] I have continued reading Chapter 4 of "Terraform: Up & Running".
- [ ] I have watched the required Udemy videos on advanced module usage.
- [ ] I have enhanced my Terraform module to support versioning and multiple environments.
- [ ] I have refactored my Terraform module for the Bonus Hands-On Project and deployed infrastructure across environments.
- [ ] I have written and published a blog post about today's task.
- [ ] I have made a social media post about today's task.
- [ ] I have created a `day9-update-your-github-username.md` file with my Terraform code and architecture diagrams.
- [ ] I have created a pull request with all the required details.

## Additional Resources

- [Terraform: Up & Running on Amazon](https://www.amazon.com/Terraform-Running-Infrastructure-Configuration-Management/dp/1492046906)
- [Udemy Course on Terraform](https://www.udemy.com/course/terraform/)
- [Terraform Module Documentation](https://www.terraform.io/docs/language/modules/index.html)
