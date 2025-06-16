#!/bin/bash
#
# Terraform v1.9.5
# ansible [core 2.17.1]
#
# Run with: sh install.sh

demo_action=$1

# Esto puede estar en tu .bashrc, sino lo descomentas y ya! 
# export TF_VAR_vpc_id="vpc-xxxxx"
# export TF_VAR_subnet_id="subnet-xxxxxxxx"

FILE=terraform/kp/demo_sshkey_tf
if [ -f "$FILE" ]; then
    echo "ssh-key	[OK]"
else 
    echo "$FILE does not exist. Create it first"
    echo "  Example: ssh-keygen -b 2048 -t rsa -f terraform/kp/demo_sshkey_tf -q -N '' "
    exit 1
fi


# Function to wait for EC2 instance and anotehr deployments
wait_for_ssh () {
    echo "Waiting for SSH port to be available on EC2..."
    ec2_host=$(terraform -chdir=terraform/ output -raw objetive)
    while ! nc -z -w 3 "$ec2_host" 22 2>/dev/null; do
        echo -n "."
        sleep 2
    done
    echo
    echo "SSH port is open. Continuing with Ansible..."
}


if [ "$demo_action" = "deploy" ]; then
    # Execute terrafomr init and plan to show info
    terraform -chdir=terraform/ init
    terraform -chdir=terraform/ plan
    # Run apply with auto-approve to avoid "yes question"
    if terraform -chdir=terraform/ apply --auto-approve; then
        echo
        echo "Terraform finish, waiting for AWS EC2..."
        echo
        echo
        #-----------------------------------------
        # PENDIENTE DE MEJORA (*)
        #-----------------------------------------
        wait_for_ssh
        #-----------------------------------------
        # Copy "template" to use in demo
        cp ansible/inventory.ini ansible/demo-inventory.ini
        # use TF output to send dns output to inventory ansible target
        terraform -chdir=terraform/ output objetive | jq -r >> ansible/demo-inventory.ini
        # ONLY FOR DEMO. to avoid modify original ansible inventory
        sed -i 's/ansible_ssh_private_key_file=..\//ansible_ssh_private_key_file=/'g ansible/demo-inventory.ini 
        chmod 400 terraform/kp/*
        # Run ansible and wait for deployment finish
        if ansible-playbook -i ansible/demo-inventory.ini ansible/main.yaml; then
            echo;echo
            echo "ONLY FOR DEMO. Enable public access (public port-forward)"
            echo;echo "  Happy demo! :D "
            echo;echo
            echo "Producer: http://$(terraform -chdir=terraform/ output objetive |jq -r ):5000"
            echo "Webserver: http://$(terraform -chdir=terraform/ output objetive |jq -r ):8080"
            echo "Grafana: http://$(terraform -chdir=terraform/ output objetive |jq -r ):3000"
            echo "RabbitMQ: http://$(terraform -chdir=terraform/ output objetive |jq -r ):15672"
            echo
        else
            echo "Ansible failed. Exiting script."
            exit 1
        fi
    else
      echo "Terraform apply failed. Exiting script."
      exit 1
    fi
# FOR DEMOS.  I like deploy and undeploy  :D 
elif [ "$demo_action" = "delete" ]; then
    terraform -chdir=terraform/ destroy --auto-approve
else
    echo "Please use: "
    echo "sh $0 deploy   # to deploy the demo"
    echo "sh $0 delete   # to delete the demo"
fi
