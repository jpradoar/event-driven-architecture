<div align="center">

# Event Driven Architecture

### 🏠 A small SaaS project for IoT

<br>
<hr>

:rocket:  <b> Build Status and info project:
<p></b>



![](https://github.com/jpradoar/event-driven-architecture/actions/workflows/producer-ci.yaml/badge.svg) 
![](https://github.com/jpradoar/event-driven-architecture/actions/workflows/consumer-ci.yaml/badge.svg)
![](https://github.com/jpradoar/event-driven-architecture/actions/workflows/dbwriter-ci.yaml/badge.svg) 
![](https://github.com/jpradoar/event-driven-architecture/actions/workflows/webserver-ci.yaml/badge.svg) 
![](https://github.com/jpradoar/event-driven-architecture/actions/workflows/k8s-event-exporter-ci.yaml/badge.svg) 
</p>
    
|Link | Desc |
|---|---|
|Project (summary)|[https://jpradoar.github.io/event-driven-architecture/](https://jpradoar.github.io/event-driven-architecture/)|
|<a href="https://github.com/users/jpradoar/projects/2/views/1" target="_blank">![](https://custom-icon-badges.demolab.com/badge/Kanban_project-blue.svg?logo=book)</a>   |Here you can see the full project roadmap and more info  |
| <a href="https://jpradoar.github.io/helm-chart/" target="_blank">![](https://custom-icon-badges.demolab.com/badge/Helm_charts-blue.svg?logo=Helm)</a>  |Personal Helm repo   |
|<a href="https://github.com/marketplace/actions/genericsemanticversion" target="_blank">![](https://custom-icon-badges.demolab.com/badge/Semantic_Version-blue.svg?logo=tag)</a>   |My own semantic version GitHub Action  |
|Github|[https://github.com/jpradoar/event-driven-architecture/](https://github.com/jpradoar/event-driven-architecture/)|




</div>

<b></b>   
    



<hr><br><br>


### :bulb: My idea
A simple excuse to learn and use Python as Pub/Sub with a message broker, in this case RabbitMQ, to provision infrastructure triggered by events like "buy a small module" and, finally, to monitor all that infrastructure. <br>
I love IoT. For this reason, this PoC is designed to simulate a "SaaS product". <br>
At the end of all this, it will provision my small IoT modules. :space_invader: <br>

<br>

### :fire: Supposed problem
💀 I need to manage a lot of inputs, and each of them will trigger different tasks, like messages, deployments, and more. Obviously I will reuse that data so other jobs can generate custom events, and finally I will use Grafana for analysis and trends.
<br>💀 Some apps have to get information, but a common problem is having or developing a lot of products with different technologies, like Node.js, Python or PHP.
<br>💀 I would like to have a shared source of data, to avoid rebuilding or writing connectors or APIs to connect components written in different technologies/languages.
<br>💀 All developers need to know which version must be fixed, or I need a person to manage the version numbers. (I would like to avoid managing them manually.)

<br>

### :checkered_flag: Objective
:heavy_check_mark: Create a simple API to centralize all "inputs" and organize workloads by queues. 
<br>:heavy_check_mark: Each microservice consumes its own queue and, if needed, can consume others too. 
<br>:heavy_check_mark: Each microservice does a specific task, <b>to avoid having "JUMBO-Pods"</b>.
<br>:heavy_check_mark: All microservices generate logs for future monitoring, analysis, improvements and troubleshooting.
<br>:heavy_check_mark: All logs must be exposed on stdout, to avoid writing data inside the container. This lets me run my pods with a read-only filesystem.
<br>:heavy_check_mark: Automate all tasks via API calls between microservices.
<br>:heavy_check_mark: Gain scalability and security by isolating each task in small actions/calls.
<br>:heavy_check_mark: Avoid tech dependencies or "human-tech dependence". Everyone can enjoy their own tech/language  *(...No, no Java, please!  :joy: )*.
<br>:heavy_check_mark: The standard (input/output) will be  [JSON](https://www.json.org/json-en.html) because it is an open standard and is easy to implement and parse.
<br>:heavy_check_mark: To manage version numbers I created a [Semantic Version GitHub Action](https://github.com/marketplace/actions/genericsemanticversion)  


### Extra features 
<br>:heavy_check_mark: <b>Safe data</b>:  My apps use tokens and passwords. I need to manage them safely and commit all the code without leaking my secrets.   ;) 
<br>:heavy_check_mark: <b>Vendor lock-in</b>: In my case, I prefer an infrastructure that can be used and implemented in any cloud provider that runs a Kubernetes cluster, in an "on-premise" client environment, or even in a development environment like my laptop.
<br>:heavy_check_mark: <b>Vulnerability Scans</b>: Every time a developer or SRE builds a Docker image, it must be scanned to find possible vulnerabilities. If any are found, that image has to be marked with a different tag. [Vulnerability Scans](vuln_scans/)  and  [HTML format](https://jpradoar.github.io/event-driven-architecture/vuln_scans/vuln_scan_demo.html)
<br>:heavy_check_mark: <b>Monitoring</b>: All developers and DevOps engineers must be able to see some metrics.
<br><hr><br>


### Infrastructure design and workflow

<div align="center">
<br><img src="img/infrastructure-diagram.jpg">
<br>
<br><img src="img/terraform-workflow.jpg">
</div>


<br><br>

### Docker workflows logic
<br><img src="img/github-event-driven-architecture-workflow.png">

<br>

### For automatic semantic release logic
```mermaid
graph LR
    A(git push) --> B>GitHub Action]
    B --> C[Get old version ]
    C --> D[1.0.0]
    B --> | git commit -m text: ...| E{Parse Trigger}
    E --> |patch: ...| F((1.0.1))
    E --> |minor: ...| G((1.1.0))
    E --> |major: ...| H((2.0.0))
    E --> |test: ... | I((1.0.0-wbp9lays))
    E --> |alpine ...| J((1.0.0-alpine))

```


# Architecture design
<br>
<img src="img/event-driven-architecture.jpg">

<br>

### JSON data model (example)
    {                                              /* Possible inputs */ 
    "client":"cliente02",                          /* Client name / identification */ 
    "namespace":"cliente02",                       /* Kubernetes namespace = client */
    "environment":"Development",                   /* Dev / Stage / Prod */
    "archtype":"SaaS",                             /* SaaS / Edge / On-Prem */
    "hardware":"Dedicated",                        /* Classic (No extra cost allocated) / Dedicated (Extra cost allocated) */
    "product":"Product-A",                         /* Product-A / -B / -C / -N */ 
    "MessageAttributes": { 
      "event_type": { 
        "Type": "String",     
        "Value": "mycompany.producer.event.client.published"   /* (Dynamic) Company.App.messageType.client.EventAction */
        }, 
      "published_on": "2023.01.2.23.02.642883101",         /* +%Y.%m.%d.%H.%M.%N */ 
      "trace_id": "9a2ae9de-3f82-4f55-966b-47df50ff51ff",  /* unique random string  */
      "retrace_intent": "0"                                /* how many retries */
      }, 
      "Metadata": { 
        "host": "hostname",                       /* microservice */
        "origing": "Cloud",                       /* Cloud / On-Prem */
        "publisher": "producer"                   /* publisherType */
      } 
    } 

### TraceID from deployment workflow to pod annotations
<br>
<img src="img/client-pod-trace_id.png"> 

_This trace_id is super useful when you need to see the deployment trace, and I also use it as a reference tag and/or annotation in pods.
The trace_id is generated on the first API call of the deployment process and is attached to all the pods. If you use Grafana or similar, you can trace all the steps and associate them with the deployment, or even with each pod deployed by this process._


<br><br>

### Producer (client portal)
<br>
<img src="img/producer.png"><img src="img/producer-2.png">
<br>

### DBClients UI (webserver)
<br>
<img src="img/webserver.png">
<br>

### Kubernetes Logs
<br>
<img src="img/consumer-logs.png">
<br>
<img src="img/full-log.png">
<br>

### Alerts and Messages
<br>
<img src="img/slack-build-msg.png">
<br>
