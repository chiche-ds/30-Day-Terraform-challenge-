# Day 10: Terraform Loops and Conditionals

## Overview

Welcome to Day 10 of the Terraform 30-Day Challenge! Today, we will dive into advanced Terraform techniques, focusing on loops and conditionals. Loops and conditionals allow you to write more dynamic and reusable Terraform configurations, enabling you to deploy resources based on varying conditions and input variables. By the end of today, you’ll have experience using `count`, `for_each`, and conditionals to simplify and automate your infrastructure deployments.

## Tasks for Today

### 1. **Reading**
   - **Chapter**: Chapter 5 (Pages 141-160)
     - Sections: "Loops with `count` and `for_each`".
   - **Goal**: Understand how loops can make your Terraform configurations more dynamic and flexible.

### 2. **Videos**
   - **Udemy**: Watch the following videos: focus on section 11 of the course. Most of what we will be doing this week is in this section
     - start with the video on input and output variables with Dynamic block. 
   - **Goal**: Learn how to implement loops and variables  in your Terraform code to create dynamic and efficient infrastructure deployments.

### 3. **Activity**
   - **Modify Existing Code**: Refactor your existing infrastructure code to use loops and conditionals. Use `count` to deploy multiple instances of the same resource, and use `for_each` to iterate over maps or lists of resources.
   - **Conditional Deployments**: Implement conditional logic to control resource deployment based on input variables (e.g., deploy resources in different regions based on a boolean variable).
   - **Goal**: Successfully use loops and conditionals to deploy dynamic infrastructure, minimizing redundancy in your Terraform code.


### 5. **Blog Post**
   - **Title**: "Mastering Loops  in Terraform"

### 6. **Social Media Post**
   - **Text**: "💡 Learned how to use loops  in Terraform for dynamic deployments! "

## How to Submit Your Work

### 1. **Create the `day10-update-your-github-username.md` File**
   - Include your Terraform code and any architecture diagrams in the markdown file.
   - Document your refactored Terraform code that uses loops and conditionals, and explain the logic behind your implementation.
   - Save the file in your `day10-loops` branch.

### 2. **Commit Your Changes**
   - Stage and commit your changes with a message like:
     ```bash
     git add day10-update-your-github-username.md
     git commit -m "Completed Day 10 task on loops "
     ```

### 3. **Create a Pull Request**
   - Push your changes to your GitHub repository:
     ```bash
     git push origin day10-loops
     ```
   - Create a pull request using the provided template and include any additional comments if necessary.

## Checklist

- [ ] I have completed Chapter 5 of "Terraform: Up & Running".
- [ ] I have watched the required Udemy videos on loops.
- [ ] I have refactored my Terraform code to use loops .
- [ ] I have written and published a blog post about today's task.
- [ ] I have made a social media post about today's task.
- [ ] I have created a `day10-update-your-github-username.md` file with my Terraform code and architecture diagrams.
- [ ] I have created a pull request with all the required details.

## Additional Resources

- [Terraform: Up & Running on Amazon](https://www.amazon.com/Terraform-Running-Infrastructure-Configuration-Management/dp/1492046906)
- [Udemy Course on Terraform](https://www.udemy.com/course/terraform/)
- [Terraform Documentation: Loops and Conditionals](https://www.terraform.io/docs/language/expressions/for.html)
