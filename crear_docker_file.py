import sys
argv = sys.argv
print("creado docker script")
print("creando: " + sys.argv[1] + "basic consumers")
print("creando: " + sys.argv[2] + "star consumers")
print("creando: " + sys.argv[3] + "text consumers")
print("creando: " + sys.argv[4] + "business consumers")
print("creando: " + sys.argv[5] + "day consumers")

f = open("docker.fake","w")
f.write('version: '+"'3'"+'\nservices:\n\
  rabbitmq:\n\
    build:\n\
      context: ./rabbitmq\n\
      dockerfile: rabbitmq.dockerfile\n\
    ports:\n\
      - 15672:15672\n\
    healthcheck:\n\
        test: ["CMD", "curl", "-f", "http://localhost:15672"]\n\
        interval: 10s\n\
        timeout: 5s\n\
        retries: 10\n\
')

f.write("\n\n  producer:\n\
    build:\n\
      context: ./producer\n\
      dockerfile: producer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    volumes:\n\
      - myvolume:/data\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - N_BASIC_CONSUMERS=" + argv[1]+ "\n\
      - N_STAR_CONSUMERS=" + argv[2] + "\n\
      - N_DAY_CONSUMERS=" + argv[5] + "\n\
      - N_TEXT_CONSUMERS=" + argv[3] + "\n\
      - N_BUSINESS_CONSUMERS=" + argv[4])


f.write("\n\n\n  business_producer:\n\
    build:\n\
      context: ./business_producer\n\
      dockerfile: business_producer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    volumes:\n\
      - myvolume:/data\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1)")

for i in range(0,int(argv[1])):
	if(argv[1] == "1"):
		id = ""
	else:
		id = str(i)
	f.write("\n\n  consumer"+id+":\n\
    build:\n\
      context: ./consumer\n\
      dockerfile: consumer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - ID="+id)


for i in range(0,int(argv[2])):
	if(argv[2] == "1"):
		id = ""
	else:
		id = str(i)
	f.write("\n\n  star_consumer" +id+  ":\n\
    build:\n\
      context: ./star_consumer\n\
      dockerfile: star_consumer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - ID=" + id )

for i in range(0,int(argv[3])):
	if(argv[3] == "1"):
		id = ""
	else:
		id = str(i)
	f.write("\n\n  text_consumer"+id+":\n\
    build:\n\
      context: ./text_consumer\n\
      dockerfile: text_consumer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - ID="+id)

  

for i in range(0,int(argv[4])):
	if(argv[4] == "1"):
		id = ""
	else:
		id = str(i)
	f.write("\n\n  business_consumer"+id+":\n\
    build:\n\
      context: ./business_consumer\n\
      dockerfile: business_consumer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - ID="+id)

for i in range(0,int(argv[5])):
	if(argv[5] == "1"):
		id = ""
	else:
		id = str(i)
	f.write("\n\n  day_consumer"+id+":\n\
    build:\n\
      context: ./day_consumer\n\
      dockerfile: day_consumer.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - ID="+id)


f.write("\n\n  sink:\n\
    build:\n\
      context: ./sink\n\
      dockerfile: sink.dockerfile\n\
    restart: on-failure\n\
    depends_on:\n\
      - rabbitmq\n\
    links: \n\
      - rabbitmq\n\
    environment:\n\
      - PYTHONUNBUFFERED=1\n\
      - N_BASIC_CONSUMERS=" + argv[1] + "\n\
      - N_STAR_CONSUMERS=" + argv[2] + "\n\
      - N_DAY_CONSUMERS=" + argv[5] + "\n\
      - N_TEXT_CONSUMERS=" + argv[3] + "\n\
      - N_BUSINESS_CONSUMERS=" + argv[4] + "\n\
\n\
volumes:\n\
  myvolume:\n\
    external: true")
f.close()