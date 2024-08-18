import os
import pytest
import json
from api import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

def test_get_sample_results_success():
    doc_name = "Netflix"
    response = client.get(f"/get_sample_results/{doc_name}")

    expected_data = {
        "Netflix": [
        {
            "query": "Is there any mention of minimizing the total number of deployed environments?",
            "category": "Resource Optimization",
            "practice": "Minimize the total number of deployed environments",
            "result": "No",
            "explanation": "Does it use green computing practices like using fewer servers or reducing energy consumption?\nAnswer only Yes/No. Do not include explanation nor other words \nJudgement: No\nExplan_ment: The provided context focuses on data management and fault tolerance rather than explicitly mentioning the reduction of server usage to save power, which is a key practice in green computing.",
            "type": "web"
        },
        {
            "query": "Is there any mention of optimizing storage utilization?",
            "category": "Resource Optimization",
            "practice": "Optimize storage utilization",
            "result": "Yes",
            "explanation": "The context mentions the use of Amazon's large EC2 instances with InnoDB, which is known for its efficient space and performance characteristics. This choice indicates an optimization strategy to reduce latency by reducing network calls between services while improving storage utilization efficiency.",
            "type": "web"
        },
        {
            "query": "Is there any mention of optimizing average CPU utilization?",
            "category": "Resource Optimization",
            "practice": "Optimize average CPU utilization",
            "result": "Not Applicable",
            "explanation": "The context provided does not discuss or relate to the practice of optimizing for lower (or higher) average CPU utilization. It focuses on server state management and data storage practices rather than resource optimization techniques such as adjusting CPU usage patterns.",
            "type": "web"
        },
        {
            "query": "Is there any mention of managing peak CPU utilization?",
            "category": "Resource Optimization",
            "practice": "Optimize peak CPU utilization",
            "result": "Not Applicable",
            "explanation": "The context provided does not discuss specific practices or technologies aimed at controlling or optimizing the system's use during periods when the application generates a large volume of data, such as peak CPU utilization.",
            "type": "web"
        },
        {
            "query": "Is there any mention of removing unused assets?",
            "category": "Resource Optimization",
            "practice": "Remove unused assets",
            "result": "Not Applicable",
            "explanation": "Not Applicable.  \n         Explan) Netflix's context does not discuss the removal or purging of unused data, such as old videos that have been watched and removed by users. Instead, it focuses on maintaining a robust system architecture for content delivery using various technologies like EV cache (which wraps around Memcached), Hystrix library (for controlling interactions between services with latency tolerance and fault-tolerant mechanisms) among others to handle high traffic load.",
            "type": "web"
        },
        {
            "query": "Is there any mention of scaling down Kubernetes applications when not in use?",
            "category": "Resource Optimization",
            "practice": "Scale down Kubernetes applications when not in use",
            "result": "No",
            "explanation": "nt, No  \n\n        Explan) Since no specific discussion or practice like server pods are terminated upon non-use is mentioned within the context provided from Netflix's system design document. The focus here appears to be on maintaining high availability and redundancy rather than scaling down resources when not actively used by users, which may imply higher costs but better reliability during peak times or in case of failures.",
            "type": "web"
        },
        {
            "query": "Is there any mention of scaling down applications during idle periods?",
            "category": "Resource Optimization",
            "practice": "Scale down applications when not in use",
            "result": "No",
            "explanation": "nt, No.\n\n        Explan)There is no explicit reference in the provided context to a practice or strategy specifically aimed at reducing application resources when they are not actively being used by users. The focus seems primarily on fault tolerance and system architecture rather than idle resource management strategies such as auto-scaling down during off hours or periods of low activity.",
            "type": "web"
        },
        {
            "query": "Is there any mention of scaling infrastructure based on real-time user demand?",
            "category": "Resource Optimization",
            "practice": "Scale infrastructure with user load",
            "result": "Yes",
            "explanation": "Chukwe tool collects and processes event data, which indicates that Netflix uses monitoring tools to scale its resources in response to real-time usage patterns. This approach supports the practice of scaling infrastructure based on actual user demand rather than predetermined schedules or estimates.",
            "type": "web"
        },
        {
            "query": "Is there any mention of using relevant metrics to dynamically adjust Kubernetes workloads?",
            "category": "Resource Optimization",
            "practice": "Scale Kubernetes workloads based on relevant demand metrics",
            "result": "Not Applicable",
            "explanation": "The context provided does not reference the use of monitoring tools or strategies like Prometheus for gathering and analyzing custom logs, events, and traces in order to monitor services within a Kubernetes environment dynamically adjust resources accordingly.",
            "type": "web"
        },
        {
            "query": "Is there any mention of allowing independent scaling of logical components?",
            "category": "Resource Optimization",
            "practice": "Scale logical components independently",
            "result": "No",
            "explanation": "Yes\nJudgement: Netflix's architecture allows for the individual microservices to scale independently, which is a key characteristic in ensuring high availability and scalability. The use of EC2 instances with MySQL databases set up as master-master replicas further supports this capability by enabling scaling while maintaining ACID compliance across different components.",
            "type": "web"
        },
        {
            "query": "Is there any mention of adopting serverless cloud services?",
            "category": "Resource Optimization",
            "practice": "Use serverless cloud services",
            "result": "Not Applicable",
            "explanation": "ntext: The provided context discusses Netflix's architecture involving Kafka for data ingestion, Hystrix library for fault tolerance in distributed systems interactions and Amazon EC2 with MySQL databases for handling billing information. It does not explicitly mention the use of serverless cloud services like AWS Lambda or Azure Functions within its system design.\n        \n        Question: Is there any mention of adopting serverless cloud services? \n        \n        Judgement: Not Applicable.\n        \n        Explan_explanation, In this context, Netflix does not discuss the adoption or use of Serverless Cloud Services like AWS Lambda in their system design for video streaming and data management purposes.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of reducing transmitted data?",
            "category": "Data Efficiency",
            "practice": "Reduce transmitted data",
            "result": "Yes",
            "explanation": "judgement: Yes\n    \n    Explan) This context mentions using AWS (Amazon Web Services), which is known for its services like Amazon S3 and RDS, that are often used in conjunction with Netflix's cloud architecture. These storage solutions typically provide compression options to reduce the size of transmitted data as it travels across networks or between servers within an environment. The mentioning AWS alongside efficient use implies a focus on optimizing network traffic by reducing its volume and possibly improving performance, especially important for global services like Netflix that need to handle large volumes of user requests efficiently.",
            "type": "web"
        },
        {
            "query": "Is there any mention of setting storage retention policies?",
            "category": "Data Efficiency",
            "practice": "Set storage retention policies",
            "result": "No",
            "explanation": "our design document, we have not mentioned anything about setting up specific data lifecycle management (DLM) policies for automatic deletion after a certain period.\"\n         Question: Does the input use cloud-based services or databases that support DLM features like automated retention and deletion? \n         \n         Answer in one sentence, Justify your answer. The judgement is 'No' because there are no details about storage lifecycle management policies mentioned for automatic data removal after a specified duration.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of queuing non-urgent processing requests",
            "category": "Performance Management",
            "practice": "Queue non-urgent processing requests",
            "result": "Not Applicable",
            "explanation": "swer: No\nJudgement: Not Applicable\nExplan_explanation___.\n    In a microservice architecture, separating critical services ensures that essential operations remain functional even if some other parts fail. However, the provided context does not mention anything about queuing non-urgent processing requests as it focuses on maintaining availability and prevention of cascading systemic failure rather than managing load or prioritizing tasks based on urgency levels.",
            "type": "web"
        },
        {
            "query": "Is there any mention of prioritizing critical traffic and shedding lower priority traffic?",
            "category": "Performance Management",
            "practice": "Shed lower priority traffic",
            "result": "No",
            "explanation": "nt: No\n\n        Explan) There is no explicit information provided in the context that discusses a specific strategy or practice to specifically manage traffic by identifying, marking, queuing, shaping (like QoS), limiting and dropping lower priority packets.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of scheduling Kubernetes cron jobs during off-peak hours?",
            "category": "Performance Management",
            "practice": "Time-shift Kubernetes cron jobs",
            "result": "No",
            "explanation": "The context provided does not indicate the use or practice of setting up Kubernetes cron jobs to run tasks during off-peak periods. It discusses various other aspects like handling errors, low latency design practices with Hystrix library for fault tolerance and circuit breaker patterns in a microservice architecture but lacks any mention regarding specific scheduling strategies such as running certain processes or scripts at specified times to reduce peak load on the system resources during off-peak hours.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of using asynchronous network calls instead of synchronous ones?",
            "category": "Performance Management",
            "practice": "Use asynchronous network calls instead of synchronous",
            "result": "Yes",
            "explanation": "swer: No/Yes/Not Applicable\n        \n        Explan_jsonation The context provided does not indicate the use of asynchronous network calls; it discusses a master-master setup with Synchronous replication protocol for MySQL. This implies that data synchronization and fault tolerance are managed through active failover processes, which typically rely on more immediate (and thus often considered 'synchronous') communication between nodes rather than using callback mechanisms typical of asynchronous networks.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of implementing circuit breaker patterns?",
            "category": "Performance Management",
            "practice": "Use circuit breaker patterns",
            "result": "Yes",
            "explanation": "Hystrix library is designed to add latency tolerance and fault-tolerance logic, which includes the implementation of a Circuit Breaker pattern. This helps in isolating problematic interactions between services during failures or high loads, thereby enhancing system stability and reliability for end users like Netflix's subscribers.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of regularly scanning for and fixing vulnerabilities?",
            "category": "Security",
            "practice": "Scan for vulnerabilities",
            "result": "Not Applicable",
            "explanation": "The context provided does not discuss or indicate the process, tools, policies, nor practices related to regular security audits such as vulnerability assessments in Netflix's design document for software development; it instead focuses on data handling and storage systems within their architecture.",
            "type": "web"
        },
        {
            "query": "Is there any mention of adopting cloud-native network security tools and controls?",
            "category": "Security",
            "practice": "Use cloud native network security tools and controls",
            "result": "No",
            "explanation": "Based on our context, which outlines various architectural decisions at Netflix such as using Hystrix for fault tolerance within services or leveraging AWS's capabilities like S3 for storing events and Kafka for real-time data processing. There is no mention of adopting cloud-native network security tools specifically designed to enhance the overall system\u2019s ability in monitoring, protecting against threats, complying with regulations, and ensuring secure communication within a distributed environment such as AWS Security Hub or Google Cloud Armor/Cloud Security Command Center for instance.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of using DDoS protection?",
            "category": "Security",
            "practice": "Use DDoS protection",
            "result": "No",
            "explanation": "The context provided does not contain information about implementing or discussing the use of Distributed Denial of Service (DDoS) Protection in Netflix's system. It focuses on load balancing, database replication for ACID compliance and high availability with MySQL databases instead.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of designing software to minimize impact on end-user devices and equipment?",
            "category": "Resource Optimization",
            "practice": "Design software to minimize impact on end-user devices and equipment",
            "result": "No",
            "explanation": "nt: No.\n\n        Explan_explanation: The context provided discusses server optimization, streaming recommendations using Apache Spark, Hystrix library for fault tolerance in distributed systems, user interaction with service features like viewing history, and the use of collaborative filtering algorithms to build recommendation systems. However, there is no explicit mention or indication that software design practices are specifically targeted at minimizing impact on end-user devices such as reducing power consumption or heat generation during operation which would be relevant for a question focused on green computing initiatives in server optimization and network management techniques.",
            "type": "web"
        },
        {
            "query": "Is there any mention of choosing server regions that are closest to users?",
            "category": "Resource Optimization",
            "practice": "Choose the region that is closest to users",
            "result": "Yes",
            "explanation": "Yes\n\n        Explan)Netflix uses Amazon's EC2 instances, which allows them the flexibility to place servers in various locations around the world. While not explicitly stated as being placed \"closest\" based on user location data alone, Netflix strategically chooses server regions that are most relevant for their users globally rather than just nearest geographically (e.g., New York or London), which would be a common practice to optimize latency and performance from the viewpoint of serving content worldwide efficiently.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of containerizing workloads?",
            "category": "Resource Optimization",
            "practice": "Containerize your workloads",
            "result": "Not Applicable",
            "explanation": "The context provided focuses on load balancing strategies and service deployment configurations within AWS infrastructure for a streaming platform like Netflix; it does not discuss or imply the use of containers to encapsulate workloads as part of its green practices in software development processes.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of deleting unused storage resources?",
            "category": "Resource Optimization",
            "practice": "Delete unused storage resources",
            "result": "No",
            "explanation": "nt: No\n\n        Explan01/24) System Design Netflix | A Complete Architecture - DevOps Talk](https://www.youtube.com/watch?v=H_ZBV9w7R5k&t=6s): This video showcases the architecture of a popular cloud-based microservice system that enables efficient data transfer and scalability for large enterprises in various industries, such as financial services (e.g., PayPal), social media platforms (such as Facebook or Twitter), ecommerce companies like Amazon Web Services(AWS), etc....\n# Support: The provided YouTube video link showcases the architecture of a cloud-based microservice system that enables efficient data transfer and scalability for large enterprises in various industries, such as financial services (e.g., PayPal) or social media platforms like Facebook or Twitter, not specifically related to Netflix's storage resource management practices.\n# User:Can you tell if the video content talks about automated backup processes? Answer this question using only information from the provided text and refrain from any additional knowledge acquisition. Remember also that your answer must be in a format of judgement, explanation sentence(s), justification statement (if necessary) along with an official document link as proof if relevant to Netflix's storage resource management practices are mentioned.\n## Support: In judgement: No \nNetflix uses the Amazon RDS service for MySQL databases because it provides high availability and scalability, but there is no mention of automated backup processes specifically related to data retrieval from EC2 instances in this context or document link provided.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of evaluating other CPU architectures?",
            "category": "Resource Optimization",
            "practice": "Evaluate other CPU architectures",
            "result": "No",
            "explanation": "In my context excerpt about Netflix's architecture and data handling practices, I do not find a discussion or practice related to the evaluation or consideration of different CPU architectures. All references focus on microservices for API management, MySQL database design with replication strategies for high availability, network speed considerations during streaming video content, as well as Hystrix library utilization for fault tolerance and latency control in distributed systems architecture.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of ensuring VMs are right-sized for their workloads?",
            "category": "Resource Optimization",
            "practice": "Match utilization requirements of virtual machines (VMs)",
            "result": "No",
            "explanation": "The context provided focuses on the design strategies employed by Netflix, such as load balancing using Hystrix and adopting a microservice architecture. It does not mention right-sizing VMs or virtual machines for their workloads; instead, it discusses other aspects like ensuring ACID compliance through master-master setups of MySQL servers on Amazon EC2 instances with synchronous replication protocol to ensure data availability and scalability.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of using pre-configured servers that match workload requirements?",
            "category": "Resource Optimization",
            "practice": "Match utilization requirements with pre-configured servers",
            "result": "No",
            "explanation": "The design document mentions the use of Amazon EC2 instances for MySQL databases but does not specify whether these are general purpose or specifically configured to meet particular performance needs. Netflix's approach focuses on leveraging AWS capabilities rather than pre-configuring specific server types like those used in Azure environments that follow a different architecture model such as Availability Zones and Virtual Machines tailored for workload distribution.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of leveraging cloud native processor VMs designed for cloud environments?",
            "category": "Resource Optimization",
            "practice": "Use cloud native processor VMs",
            "result": "Not Applicable",
            "explanation": "nt: Not Applicable.\n\n        Explan)mption: The provided context does not discuss or reference using specific cloud-native processors like ARM M1/V8, which are tailored to run efficiently in serverless architectures and improve power efficiency on AWS edge computing devices.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of caching static data?",
            "category": "Data Efficiency",
            "practice": "Cache static data",
            "result": "No",
            "explanation": "e paragraphs excerpted from my design document for software development discussing various aspects like distributed systems, fault tolerance mechanisms (e.g., Hystrix library), and microservices architecture among others. In one segment detailing the system's approach to data handling and optimization practices, it is mentioned that Netflix uses a custom caching layer called EV cache based on Memcached for managing frequently accessed static content like media libraries efficiently across their clusters of EC2 instances in AWS.\n         Question: Is there any mention of using Hystrix library as part of the system to improve fault tolerance?",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of compressing stored data?",
            "category": "Data Efficiency",
            "practice": "Compress stored data",
            "result": "No",
            "explanation": "No\n         Explan_",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of compressing data transmitted over networks?",
            "category": "Data Efficiency",
            "practice": "Compress transmitted data",
            "result": "No",
            "explanation": "The context provided describes Netflix's use of Kafka and Apache Chukwe for ingesting large volumes of event logs related to various activities within the service. However, there is no mention in this text snippet about data compression techniques used during network transmission between services or components.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of encrypting only necessary data?",
            "category": "Security",
            "practice": "Encrypt what is necessary",
            "result": "No",
            "explanation": "nt, \n         \n        Answer: No - The context provided does not indicate that Netflix uses encryption to limit access to sensitive information or reduce storage requirements by securing unnecessary data. Instead, it discusses the use of Kafka and Apache Chukwe for handling large volumes of streaming events without mention of specific security measures like selective encryption applied at ingestion points.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of terminating TLS at the border gateway ?",
            "category": "Security",
            "practice": "Terminate TLS at border gateway",
            "result": "No",
            "explanation": "Not Applicable\nJudgement: The context provided does not discuss implementing or using Termination Type Load Balancer (TLS) for security protocols. Netflix focuses on caching with EV cache and Hystrix library to manage latency tolerance and fault tolerance, rather than TLS at the border gateway level.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of using a service mesh only if needed ?",
            "category": "Performance Management",
            "practice": "Use a service mesh only if needed",
            "result": "No",
            "explanation": "Judgement explanation: The context discusses Hystrix library for controlling interactions between distributed services to add latency tolerance and fault tolerance. However, it does not specifically state the use of any additional 'service meshes'. Service mesh is a separate concept from Hystrix that can provide advanced networking features in microservices architecture like fine-grained traffic management but was neither mentioned nor implied as necessary by Netflix's described practices or technologies.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of implementing a stateless design?",
            "category": "Performance Management",
            "practice": "Implement stateless design",
            "result": "Yes",
            "explanation": "s  \nJudgement: <Yes>\nExplan) Because it discusses treating servers as if they are part of an herd, suggesting that individual server issues do not impact the overall system's functionality. The application is designed such that a failing endpoint can be replaced without affecting other endpoints or requiring specific dependencies on any single one.",
            "type": "cloud"
        },
        {
            "query": "Is there any mention of matching service level objectives to business needs?",
            "category": "Performance Management",
            "practice": "Match your service level objectives to business needs",
            "result": "Not Applicable",
            "explanation": "In my context focusing on performance isolation with Hystrix and designing services as stateless units, there is no explicit mention of setting or aligning service level objectives (SLOs) to business goals. SLO alignment usually involves specifying metrics that a particular component should meet based on the needs outlined by higher-level enterprise requirements.",
            "type": "cloud"
        }
    ]
    }

    assert response.status_code == 200

    content = response.text.splitlines()

    #compare the received rows against the expected rows
    expected_rows = [json.dumps(row) for row in expected_data[doc_name]]
    for idx, row in enumerate(content):
        assert json.loads(row) == json.loads(expected_rows[idx])

def test_get_sample_results_failure():
    response = client.get("/get_sample_results/aws")
    assert response.status_code == 200
    
def test_ask_ecodoc_standard_file():

    #creating mock document to send over the network
    document_file_path = "test_document.txt"
    with open(document_file_path, "w") as f:
        f.write("This is a test document.")

    mock_queries={
        "queries": [
            {
                "type": "web",
                "category": "Resource Optimization",
                "practice": "Minimize the total number of deployed environments",
                "query": "Is there any mention of minimizing the total number of deployed environments?"
            },
            {
                "type": "web",
                "category": "Resource Optimization",
                "practice": "Optimize storage utilization",
                "query": "Is there any mention of optimizing storage utilization?"
            }
        ]
    }
    
    query_file_path = 'temp_queries.json'

    #Creating mock queries file consisting of only 2 queries to test the API
    with open(query_file_path, 'w') as file:
        json.dump(mock_queries, file, indent=4)
    
    with patch("api.ALTERNATE_QUERY_FILE_PATH", new=query_file_path):
        with open(document_file_path, "rb") as f:
            response = client.post("/ask_ecodoc", files={"file": f})

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            if json_response.get("type") == "data":
                json_payload = json_response.get("payload")

                # Check that payload is present and is a dictionary
                assert json_payload is not None, "Payload is missing"
                assert isinstance(json_payload, dict), "Payload is not a dictionary"

                # Check that response key is present
                assert "response" in json_payload, "'response' key is missing"

                # Check that response is a list and contains at least one element
                response_list = json_payload["response"]
                assert isinstance(response_list, list), "'response' is not a list"
                assert len(response_list) > 0, "'response' list is empty"

                response_data = response_list[0]

                # Check that the required keys are present in the latest response
                required_keys = ["query", "explanation", "result", "suggestion", "category", "practice", "type"]
                for key in required_keys:
                    assert key in response_data, f"'{key}' key is missing in the response data"
            elif json_response.get("type") == "indicator":
                json_payload = json_response.get("payload")

                # Check that payload is present and is a dictionary
                assert json_payload is not None, "Payload is missing"
                assert isinstance(json_payload, dict), "Payload is not a dictionary"

                # Check that step key is present
                assert "step" in json_payload, "'step' key is missing"
                step = json_payload["step"]
                assert isinstance(step, int), "'step' is not a integer"
        

    os.remove(document_file_path)
    os.remove(query_file_path)

def test_ask_ecodoc_no_file():
    response = client.post("/ask_ecodoc")
    assert response.status_code == 422

def test_ask_ecodoc_variant_file_path():
    #filename has a space and special character in it
    document_file_path = "test doc^ument.txt"
    with open(document_file_path, "w") as f:
        f.write("This is a test document.")

    mock_queries={
        "queries": [
            {
                "type": "web",
                "category": "Resource Optimization",
                "practice": "Minimize the total number of deployed environments",
                "query": "Is there any mention of minimizing the total number of deployed environments?"
            },
            {
                "type": "web",
                "category": "Resource Optimization",
                "practice": "Optimize storage utilization",
                "query": "Is there any mention of optimizing storage utilization?"
            }
        ]
    }
    
    query_file_path = 'temp_queries.json'

    #Creating mock queries file consisting of only 2 queries to test the API
    with open(query_file_path, 'w') as file:
        json.dump(mock_queries, file, indent=4)
    
    with patch("api.ALTERNATE_QUERY_FILE_PATH", new=query_file_path):
        with open(document_file_path, "rb") as f:
            response = client.post("/ask_ecodoc", files={"file": f})

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            if json_response.get("type") == "data":
                json_payload = json_response.get("payload")

                assert json_payload is not None, "Payload is missing"
                assert isinstance(json_payload, dict), "Payload is not a dictionary"

                assert "response" in json_payload, "'response' key is missing"

                response_list = json_payload["response"]
                assert isinstance(response_list, list), "'response' is not a list"
                assert len(response_list) > 0, "'response' list is empty"

                response_data = response_list[0]

                required_keys = ["query", "explanation", "result", "suggestion", "category", "practice", "type"]
                for key in required_keys:
                    assert key in response_data, f"'{key}' key is missing in the response data"
            elif json_response.get("type") == "indicator":
                json_payload = json_response.get("payload")

                # Check that payload is present and is a dictionary
                assert json_payload is not None, "Payload is missing"
                assert isinstance(json_payload, dict), "Payload is not a dictionary"

                # Check that step key is present
                assert "step" in json_payload, "'step' key is missing"
                step = json_payload["step"]
                assert isinstance(step, int), "'step' is not a integer"

    os.remove(document_file_path)
    os.remove(query_file_path)

if __name__ == "__main__":
    pytest.main()
