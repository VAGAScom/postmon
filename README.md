Postmon [<img src="https://api.travis-ci.org/PostmonAPI/postmon.svg?branch=master" />](http://travis-ci.org/PostmonAPI/postmon) [![Coverage Status](https://coveralls.io/repos/github/PostmonAPI/postmon/badge.svg?branch=master)](https://coveralls.io/github/PostmonAPI/postmon?branch=master) [![Support via Gratipay](
https://img.shields.io/gratipay/team/postmon.svg)](https://gratipay.com/postmon/)
==========

API para consulta de CEP's e relacionados

Requisitos do ambiente de desenvolvimento
---------------------------------------------
* MongoDB
* Python 2.7
* iPython (recomendado)

Requisitos do ambiente Python
-----------------------

As dependências estão listadas no arquivo requirements.txt.

* requests
* lxml
* pymongo
* bottle
* nosetests
* webtest
* packtrack
* celery

Rodando testes
----------------
Executar o comando:

	make test

na raiz do projeto.

Rodando a aplicação localmente na porta 9876
--------------------------------

	$ python PostmonServer.py

ou

	$ ipython -i PostmonServer.py
	>> _standalone()

Caso queira rodar em outra porta, basta passá-la como parametro no chamado do _standalone

Para rodar o [Scheduler](#scheduler):

	$ celery worker -B -A PostmonTaskScheduler -l info

Recomenda-se a utilização do [Supervisord](http://supervisord.org/) para manter o Celery rodando. Exemplo de configuração para o _supervisord.conf_:

	[program:celeryd]
	command=celery worker -B -A PostmonTaskScheduler -l info
	directory=POSTMON_HOME/repositorio
	stdout_logfile=POSTMON_LOG_DIR/celeryd.log
	stderr_logfile=POSTMON_LOG_DIR/celeryd_err.log
	autostart=true
	autorestart=true
	startsecs=10
	stopwaitsecs=600

Executando a aplicação no Docker
------------------------

Se você tem o Docker instalado, pode fazer o build da imagem e rodar o Postmon em um container.

```bash
$ docker build -t postmon .
$ docker run -d -p 80:9876 postmon
```

Acesse o endereço `http://<endereço-do-servidor-docker>/v1/cep/<cep-a-consultar>`, por exemplo `http://127.0.0.1/v1/cep/01311940`.

Configuração do Airbrake
------------------------

O [Airbrake](https://airbrake.io/) pode ser utilizado para monitorar os erros na chamado dos Correios para a verificação de CEP, para tanto as seguintes variáveis de ambiente do sistema operacional devem ser preenchidas:

- **AIRBRAKE_PROJECT_ID**: código do projeto cadastrado no Airbrake
- **AIRBRAKE_API_KEY**: chave de acesso do cadastrado do projeto no Airbrake
- **AIRBRAKE_ENVIRONMENT**: ambiente no qual a aplicação esta sendo executada (development, staging, production, etc)

MongoDB com autenticação
------------------------

Se o seu MongoDB possui autenticação habilitada você deverá configurar o banco do postmon
e também exportar duas variavéis de ambiente.

```javascript
mongo
> use postmon
> db.addUser('admin', '123456')
```

Agora que seu Mongo está com password exporte as variaveis de ambiente.

```bash
export POSTMON_DB_USER=admin
export POSTMON_DB_PASSWORD=123456
```

Para conectar em um banco remoto exporte a variável de ambiente:
```bash
export POSTMON_DB_HOST=<IP_DO_SERVIDOR>
```

Caso você queira se conectar a um replica set do mongo, separe os hosts por *,* (virgulas):
```bash
export POSTMON_DB_HOST=<IP_DO_SERVIDOR_1>,<IP_DO_SERVIDOR_2>,...,<IP_DO_SERVIDOR_N>
```


Scheduler
---------

O Postmon conta com um scheduler baseado na ferramenta [Celery](http://www.celeryproject.org/). Até o momento, a única funcionalidade implementada nessa estrutura é a rotina de coleta de dados do [IBGE](#ibge).

O Celery usa, como Broker, a mesma instância do MongoDB utilizada no módulo de CEP.

O comando apresentado na seção [rodando a aplicação](#rodando-a-aplicação-localmente-na-porta-9876) pode ser quebrado em dois caso seja necessário rodar o Celery Worker separado do Celery Beat. Para mais informações sobre essa questão leia a [documentação do Celery](http://docs.celeryproject.org/en/latest/).

Além do Broker, o Celery Beat depende internamente de uma base de dados, criada automaticamente na primeira execução, onde são armazenadas informações sobre os schedules. Por padrão essa base fica em um arquivo chamado _celerybeat_schedule_, criado no diretório onde o Celery Beat foi executado. Esse local pode ser alterado através do switch -s, conforme exemplo abaixo:

	$ celery worker -B -A PostmonTaskScheduler -l info -s /novo/caminho/para/arquivo/celerybeat_schedule

IBGE
-------------

O Postmon fornece as seguintes informações extraídas do site do IBGE:

* Código do município/UF
* Área territorial (em km²)

Essas informações estão presentes nos atributos *estado_info* e *cidade_info* da rota de busca de _cep_, bem como nas seguintes rotas:

* /uf/{sigla-uf}
* /cidade/{sigla-uf}/{nome-cidade}

Exemplos:

* /uf/SP
* /cidade/SP/São Paulo
* /cidade/SP/Araraquara
* /cidade/RJ/Macaé

A rotina de atualização desses dados está configurada para rodar diariamente.

    Postmon - The Mongo Postman API
    Copyright (C) 2013  Coding For Change

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
