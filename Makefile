run:
	docker run -it -d --env-file .env --restart=unless-stopped --name gpt_container gpt_bot
stop:
	docker stop easy_refer
attach:
	docker attach easy_refer
dell:
	docker rm easy_refer