### **# Day 27: 3-Tier Multi-Region High Availability Infrastructure with AWS and Terraform**

#### **Participant Details**
- **Name:** Yusuf Abdulganiyu  
- **Task Completed:**  
  Today, I tackled the challenge of building a **3-tier multi-region high-availability infrastructure** using AWS and Terraform. This architecture was designed for production readiness, ensuring fault tolerance and high availability by distributing workloads across multiple AWS availability zones, and cross region snapshot backup.  

  The project involved deploying key components like Elastic Load Balancers, EC2 Auto Scaling Groups, and RDS databases with multi-az read replicas. By leveraging Terraform’s modular approach and AWS best practices, I was able to create a scalable, secure, and resilient infrastructure to handle enterprise workloads effectively.  

#### **Activities**
1. **Reading**  
   - Reviewed relevant sections in the Terraform documentation:  
      - **VPC and EC2**: Best practices for networking and compute resources.  
      - **Elastic Load Balancer (ELB)**: Configuration for distributing web traffic.  
      - **Auto Scaling**: Strategies for scaling application instances dynamically.  
      - **RDS Multi-AZ and Cross-Region Read Replicas**: Ensuring database availability and failover.  

2. **Implementation Tasks**
   - **Web Tier**:  
      - Deployed Elastic Load Balancer (ELB) in public subnets to route traffic effectively.  
      - Configured health checks for improved fault tolerance.  

   - **Application Tier**:  
      - Launched EC2 instances in private subnets to handle application logic.  
      - Configured an Auto Scaling Group (ASG) to adjust capacity based on demand.  

   - **Database Tier**:  
      - Deployed a primary RDS instance with Multi-AZ support.  
      - Configured cross-region snap shot backup, and multi az read replicas and standby to ensure database failover capabilities.  

#### **Reflections**
Today’s activity reinforced the importance of modularity and best practices in building complex cloud architectures. The multi-region approach demonstrated how Terraform simplifies managing infrastructure across multiple AWS regions, enabling scalability and disaster recovery.  

The most rewarding part of this exercise was integrating Terraform modules to streamline the setup process, ensuring consistent and reusable code. Achieving high availability and fault tolerance at the infrastructure level feels like a significant step forward in my Terraform journey.  

🚀 Building this architecture was both challenging and rewarding, providing valuable insights into real-world production scenarios.  

#### **Date and Time**
- January 5, 2025, 20:14 🕙 GMT+1  

#### **Additional Notes**
- Mastered AWS multi-region strategies for fault tolerance and scalability.  
- Learned how to configure Route 53 for automated DNS failover.  
- Applied Terraform’s modular design to simplify the management of multi-tier infrastructures.  
