#!/bin/bash
#
# Terraform v1.9.5
# ansible [core 2.17.1]
#
# Run with: sh install.sh

sleep_time="210"
demo_action=$1

# Esto puede estar en tu .bashrc, sino lo descomentas y ya! 
# export TF_VAR_vpc_id="vpc-xxxxx"
# export TF_VAR_subnet_id="subnet-xxxxxxxx"


# Function to wait for EC2 instance and anotehr deployments
sleep_time_4_demo () {
    for i in $(seq 1 $sleep_time); do
        echo -n "."
        sleep 1
    done
    echo;
}


if [ "$demo_action" = "deploy" ]; then
    # Execute terrafomr init and plan to show info
    terraform -chdir=terraform/ init
    terraform -chdir=terraform/ plan
    # Run apply with auto-approve to avoid "yes question"
    if terraform -chdir=terraform/ apply --auto-approve; then
        echo
        echo "Terraform finish, waiting for AWS EC2..."
        echo;echo
        echo "waiting $sleep_time seconds"
        #-----------------------------------------
        # PENDIENTE DE MEJORA (*)
        #-----------------------------------------
        sleep_time_4_demo
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
            echo
            echo "wait for running kubernetes pods"
            sleep_time_4_demo
            echo "ONLY FOR DEMO. Enable public access (public port-forward)"
            #ansible-playbook -i ansible/demo-inventory.ini ansible/kubectl-port-forward.yaml
            echo;echo "  Happy demo! :D "
            echo;echo
            echo "Producer: http://$(terraform -chdir=terraform/ output objetive |jq -r ):5000"
            echo "Webserver: http://$(terraform -chdir=terraform/ output objetive |jq -r ):8080"
            echo "Grafana: http://$(terraform -chdir=terraform/ output objetive |jq -r ):3000"
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


#-------------------------
# MEJORA (*)
#-------------------------
# Problema: La EC2 tarda X tiempo en estar operativa.
# 
# Solución:
# Para evitar tener que esperar siempre el $sleep_time
# lo ideal seria reemplazar el sleep por una funcion que
# valide si el puerto está abierto, mientras este cerrado,
# que se quede loopeando, hasta que el puerto se abra
# y ejeute el comando de ansible
# 
# # Validar el puerto abierto: 
# "nc -vz $(terraform -chdir=terraform/  output objetive|jq -r .) 22"
#
