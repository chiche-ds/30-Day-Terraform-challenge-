# Day 12: Zero-Downtime Deployment with Terraform


## Participant Details

- **Name:** BOROHOUL Soguelni Malachie
- **Task Completed:** I completed the chapter and understood the concepts of zero-downtime deployments
- **Date and Time:** 9/02/2024 00:03 PM 

## Terraform Code 

## Architecture 
[Initially, you have the original ASG running v1 of your code.](https://asset.cloudinary.com/dshli1qgh/93d797c4a1ec8b73c7dc4cbc2bb7d20e)
[Terraform begins deploying the new ASG with v2 of your code](https://asset.cloudinary.com/dshli1qgh/e3604a6006c3736d07340c3f279d960e)
[The servers in the new ASG boot up, connect to the DB, register in the ALB, and begin serving traffic](https://asset.cloudinary.com/dshli1qgh/78358b3225bfacf9f364d1e0b2037f40)
[The servers in the old ASG begin to shut down.](https://asset.cloudinary.com/dshli1qgh/b471eb72c4b95396ad6ff27f7c86f883)
[Now, only the new ASG remains, which is running v2 of your code](https://asset.cloudinary.com/dshli1qgh/91a03202b1fd839108e659bc875b0ab3)


