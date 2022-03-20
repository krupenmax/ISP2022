build:
	sudo docker build -t lab_1 .
run:
	sudo docker run --rm -it --name lab_1 -v "/home/krupen/PycharmProjects/LB1/":/lab_1 lab_1:latest
stop:
	sudo docker stop lab_1