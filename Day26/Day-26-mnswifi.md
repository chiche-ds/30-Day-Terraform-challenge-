### **# Day 26: Build a Scalable Web Application with Auto Scaling on AWS**

#### **Participant Details**  
- **Name:** Yusuf Abdulganiyu  
- **Task Completed:**  
  Today, I deployed a scalable web application on AWS using Terraform. The project utilized key AWS resources, including Launch template for EC2 instances launch, an Elastic Load Balancer (ELB), and an Auto Scaling Group (ASG) to ensure high availability and elasticity. Following Terraform best practices, I used modular code, remote state management with S3 and DynamoDB, and version-controlled workflows for efficient and maintainable infrastructure management.

#### **Activities**  
1. **Reading**  
   - Reviewed documentation on AWS Auto Scaling Groups and Elastic Load Balancers.  
   - **Key Takeaways:**  
      - ELB ensures traffic is evenly distributed across instances and enhances fault tolerance.  
      - Auto Scaling adjusts EC2 instances based on defined policies, reducing costs and ensuring optimal performance.  
      - Using Terraform modules promotes reusable and modular code for scalable infrastructure.  

2. **Practical Activity**  
   - **Terraform Modules:**  
     - Created reusable modules for EC2 instances, ELB, and Auto Scaling Groups.  
     - Ensured all resources followed the DRY principle and modular structure.  

   - **Infrastructure Setup:**  
     - Deployed EC2 instances running a web application with appropriate security groups to allow HTTP/HTTPS traffic.  
     - Configured an ELB to distribute incoming traffic across the instances, ensuring fault tolerance.  
     - Set up an Auto Scaling Group to dynamically manage the number of EC2 instances based on traffic and CPU utilization.  
     - Configured health checks to monitor the instances' status via ELB.  

   - **Remote State Management:**  
     - Stored Terraform state files in an S3 bucket.  
     - Enabled state locking and consistency using a DynamoDB table.  

3. **Git Integration:**  
   - Committed changes incrementally to track progress and ensure code safety.  

#### **Reflections**  
Today's task demonstrated how to leverage AWS's scalable services with Terraform to build reliable and flexible infrastructure. Setting up a Load Balancer and Auto Scaling Group allowed me to see how these components come together to deliver a seamless, scalable web application experience. The integration of remote state management highlighted the importance of maintaining consistent and secure infrastructure workflows.  

💡 The highlight of the day was creating a modular project structure that can be reused for similar deployments in the future. This approach greatly simplifies infrastructure management and aligns with Terraform best practices.

#### **Date and Time**  
- December 28, 2024, 22:14 🕙 GMT+1  

#### **Additional Notes**  
- Learned how to define scaling policies in Auto Scaling Groups based on metrics such as CPU utilization.  
- Enhanced the infrastructure with robust state management using S3 and DynamoDB.  
- Realized the importance of using ELB health checks for accurate instance monitoring in Auto Scaling workflows.  

🚀 Excited to keep building scalable and robust infrastructures!
