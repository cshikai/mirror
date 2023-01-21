from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource, ResourceType

def alter_kafka_resource(topic_name: str):
    admin_client = AdminClient({'bootstrap.servers':'broker:29092'})
    topic_config = ConfigResource(ResourceType.TOPIC, topic_name)
    
    returned_config_resources = admin_client.describe_configs([topic_config], request_timeout=5)
    print(returned_config_resources)

    # new_topic_config = update the config dict associated with the Config Resource of the given Topic.
    
    updated_config_resources = admin_client.alter_configs([new_topic_config])
    print(updated_config_resources)

def delete_topic():
    admin_client = AdminClient({'bootstrap.servers':'broker:29092'})
    
    current_topics = admin_client.list_topics().topics
    print(f"current topics: {current_topics}")

    deleted_topics = admin_client.delete_topics(['queue-upload-semantic-text'])
    print(f"deleted topics: {deleted_topics}")

if __name__ == "__main__":
    delete_topic()
