 ⚠️ Body não é JSON válido: Expecting value: line 1 column 1 (char 0)
2026-03-03T17:29:48.2329716Z 2026-03-03 17:29:48,232 - api.webhook - INFO - 🔄 Tentando parsear como form-data...
2026-03-03T17:29:48.2350398Z 2026-03-03 17:29:48,234 - api.webhook - INFO - ✅ Body parseado como form-data com sucesso
2026-03-03T17:29:48.2350591Z 2026-03-03 17:29:48,234 - api.webhook - INFO - 📥 Payload parseado:
2026-03-03T17:29:48.2350712Z 2026-03-03 17:29:48,235 - api.webhook - INFO - {
2026-03-03T17:29:48.2350732Z   "action": "",
2026-03-03T17:29:48.235078Z   "webhookURL": "https://webhook-stone.azurewebsites.net/api/v1/webhook/jotform",
2026-03-03T17:29:48.2350797Z   "username": "!team_260064573416051",
2026-03-03T17:29:48.2350812Z   "formID": "253594218352056",
2026-03-03T17:29:48.2350827Z   "type": "WEB",
2026-03-03T17:29:48.2350843Z   "customParams": "",
2026-03-03T17:29:48.2350858Z   "product": "",
2026-03-03T17:29:48.2350877Z   "formTitle": "Formulário de Inscrição",
2026-03-03T17:29:48.2350891Z   "customTitle": "",
2026-03-03T17:29:48.2350905Z   "submissionID": "6483681866127454931",
2026-03-03T17:29:48.2350919Z   "event": "",
2026-03-03T17:29:48.2350932Z   "documentID": "",
2026-03-03T17:29:48.2350945Z   "teamID": "",
2026-03-03T17:29:48.2350974Z   "subject": "",
2026-03-03T17:29:48.2350988Z   "isSilent": "",
2026-03-03T17:29:48.2351001Z   "customBody": "",
2026-03-03T17:29:48.2351081Z   "rawRequest": "{\"slug\":\"submit\\/253594218352056\",\"uploadServerUrl\":\"https:\\/\\/freehelper.jotform.com\\/upload\",\"jsExecutionTracker\":\"build-date-1772558705337=>init-started:1772558706971=>validator-called:1772558706996=>validator-mounted-false:1772558706998=>init-complete:1772558707034=>interval-complete:1772558728030=>observerSubmitHandler_received-submit-event:1772558985348=>submit-validation-passed:1772558985567=>observerSubmitHandler_validation-passed-submitting-form:1772558985692\",\"submitSource\":\"form\",\"submitDate\":\"1772558985692\",\"buildDate\":\"1772558705337\",\"q6_nomeCompleto6\":{\"first\":\"Jos\\u00e9 F\\u00e1bio \",\"last\":\"Pereira do Nascimento \"},\"q7_email7\":\"josefabioo17052005@gmail.com\",\"q8_telefonecom\":{\"area\":\"81\",\"phone\":\"999888559\"},\"q9_cpf\":\"01135299455\",\"q10_voceVeio\":[\"Recome\\u00e7ar\"],\"q14_cidade\":\"Olinda \",\"q16_estado\":\"Pernambuco\",\"q17_idade\":\"35 a 44 anos\",\"q18_genero\":\"Masculino\",\"q19_escolaridade\":\"Ensino M\\u00e9dio Completo\",\"q20_faixaDe\":\"Entre 1 e 2 sal\\u00e1rios m\\u00ednimos\",\"q22_tempoDe\":\"Menos de 6 meses\",\"q23_segmentoDe\":\"Outros\",\"q25_consentimentoPara\":\"Aceito\",\"q26_declaroQue\":\"Sim\",\"newCardFormMobile\":\"1\",\"event_id\":\"1772558706972_253594218352056_uvDpbex\",\"timeToSubmit\":\"20\",\"enterprise_server\":\"freehelper.jotform.com\",\"validatedNewRequiredFieldIDs\":\"{\\\"new\\\":1,\\\"id_6\\\":\\\"Pe\\\",\\\"id_7\\\":\\\"jo\\\",\\\"id_8\\\":\\\"99\\\",\\\"id_9\\\":\\\"01\\\",\\\"id_10\\\":\\\"N\\u00e3\\\",\\\"id_14\\\":\\\"Ol\\\",\\\"id_16\\\":\\\"To\\\",\\\"id_17\\\":\\\"Ac\\\",\\\"id_18\\\":\\\"Pr\\\",\\\"id_19\\\":\\\"Do\\\",\\\"id_20\\\":\\\"Ac\\\",\\\"id_22\\\":\\\"Ma\\\",\\\"id_25\\\":\\\"Ac\\\",\\\"id_26\\\":\\\"Si\\\"}\",\"path\":\"\\/submit\\/253594218352056\"}",
2026-03-03T17:29:48.2351096Z   "fromTable": "",
2026-03-03T17:29:48.2351109Z   "appID": "",
2026-03-03T17:29:48.2351168Z   "pretty": "Nome completo::José Fábio  Pereira do Nascimento , E-mail::josefabioo17052005@gmail.com, Telefone (com DDD)::81 999888559, CPF::01135299455, Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?:Recomeçar, Cidade::Olinda , Estado::Pernambuco, Idade::35 a 44 anos, Gênero::Masculino, Escolaridade::Ensino Médio Completo, Faixa de Renda Familiar Mensal::Entre 1 e 2 salários mínimos, Tempo de funcionamento do negócio::Menos de 6 meses, Segmento de atuação::Outros, Consentimento para uso de dados pessoais.:Aceito, Declaro que todas as informações fornecidas são verdadeiras e estou ciente das condições do programa.:Sim",
2026-03-03T17:29:48.2351182Z   "unread": "",
2026-03-03T17:29:48.2351196Z   "parent": "",
2026-03-03T17:29:48.2351209Z   "ip": "181.77.118.216"
2026-03-03T17:29:48.2351222Z }
2026-03-03T17:29:48.2351273Z 2026-03-03 17:29:48,235 - api.webhook - INFO - ================================================================================
2026-03-03T17:29:48.2351804Z 2026-03-03 17:29:48,235 - api.webhook - INFO - 🔄 Detectado formato form-data do Jotform com rawRequest
2026-03-03T17:29:48.2351907Z 2026-03-03 17:29:48,235 - api.webhook - INFO - 📋 Metadados: formID=253594218352056, submissionID=6483681866127454931
2026-03-03T17:29:48.2352195Z 2026-03-03 17:29:48,235 - api.webhook - INFO - ✅ rawRequest parseado com sucesso
2026-03-03T17:29:48.2380528Z 2026-03-03 17:29:48,236 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2026-03-03T17:29:48.2384226Z 2026-03-03 17:29:48,235 - api.webhook - INFO - ✅ Campos mapeados com sucesso
2026-03-03T17:29:48.2384427Z 2026-03-03 17:29:48,235 - api.webhook - INFO - 📦 Payload mapeado:
2026-03-03T17:29:48.238445Z 2026-03-03 17:29:48,235 - api.webhook - INFO - {
2026-03-03T17:29:48.2384467Z   "Nome": {
2026-03-03T17:29:48.2384486Z     "first": "José Fábio ",
2026-03-03T17:29:48.2384504Z     "last": "Pereira do Nascimento "
2026-03-03T17:29:48.2384519Z   },
2026-03-03T17:29:48.2384537Z   "E-mail": "josefabioo17052005@gmail.com",
2026-03-03T17:29:48.2384552Z   "Telefone": {
2026-03-03T17:29:48.2384568Z     "area": "81",
2026-03-03T17:29:48.2384585Z     "phone": "999888559"
2026-03-03T17:29:48.2384614Z   },
2026-03-03T17:29:48.2384632Z   "CPF": "01135299455",
2026-03-03T17:29:48.2384654Z   "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Recomeçar",
2026-03-03T17:29:48.238467Z   "Cidade": "Olinda ",
2026-03-03T17:29:48.2384687Z   "Estado": "Pernambuco",
2026-03-03T17:29:48.2384704Z   "Idade": "35 a 44 anos",
2026-03-03T17:29:48.2384723Z   "Gênero": "Masculino",
2026-03-03T17:29:48.2384741Z   "Escolaridade": "Ensino Médio Completo",
2026-03-03T17:29:48.238476Z   "Faixa de renda familiar mensal": "Entre 1 e 2 salários mínimos",
2026-03-03T17:29:48.2384779Z   "Tempo de funcionamento do negócio": "Menos de 6 meses",
2026-03-03T17:29:48.2384799Z   "Segmento de atuação": "Outros",
2026-03-03T17:29:48.2384816Z   "submissionID": "6483681866127454931",
2026-03-03T17:29:48.2384852Z   "formID": "253594218352056"
2026-03-03T17:29:48.2384868Z }
2026-03-03T17:29:48.238489Z 2026-03-03 17:29:48,235 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:29:48.2384911Z 2026-03-03 17:29:48,235 - api.webhook - INFO - 📦 Payload final para processar:
2026-03-03T17:29:48.2384928Z 2026-03-03 17:29:48,235 - api.webhook - INFO - {
2026-03-03T17:29:48.2384944Z   "Nome": {
2026-03-03T17:29:48.2384963Z     "first": "José Fábio ",
2026-03-03T17:29:48.2384979Z     "last": "Pereira do Nascimento "
2026-03-03T17:29:48.2384994Z   },
2026-03-03T17:29:48.2385011Z   "E-mail": "josefabioo17052005@gmail.com",
2026-03-03T17:29:48.2385027Z   "Telefone": {
2026-03-03T17:29:48.2385057Z     "area": "81",
2026-03-03T17:29:48.2385073Z     "phone": "999888559"
2026-03-03T17:29:48.2385089Z   },
2026-03-03T17:29:48.2385106Z   "CPF": "01135299455",
2026-03-03T17:29:48.2385126Z   "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Recomeçar",
2026-03-03T17:29:48.2385142Z   "Cidade": "Olinda ",
2026-03-03T17:29:48.2385158Z   "Estado": "Pernambuco",
2026-03-03T17:29:48.2385173Z   "Idade": "35 a 44 anos",
2026-03-03T17:29:48.2385189Z   "Gênero": "Masculino",
2026-03-03T17:29:48.2385206Z   "Escolaridade": "Ensino Médio Completo",
2026-03-03T17:29:48.2385225Z   "Faixa de renda familiar mensal": "Entre 1 e 2 salários mínimos",
2026-03-03T17:29:48.2385257Z   "Tempo de funcionamento do negócio": "Menos de 6 meses",
2026-03-03T17:29:48.2385274Z   "Segmento de atuação": "Outros",
2026-03-03T17:29:48.2385292Z   "submissionID": "6483681866127454931",
2026-03-03T17:29:48.2385308Z   "formID": "253594218352056"
2026-03-03T17:29:48.2385323Z }
2026-03-03T17:29:48.2385343Z 2026-03-03 17:29:48,235 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:29:48.2385364Z 2026-03-03 17:29:48,235 - api.webhook - INFO - ✅ Payload validado com sucesso
2026-03-03T17:29:48.2385387Z 2026-03-03 17:29:48,235 - api.webhook - INFO - ✅ Dados processados: Nome=José Fábio Pereira do Nascimento, Telefone=(81) 999888559
2026-03-03T17:29:48.2385407Z 2026-03-03 17:29:48,236 - api.webhook - INFO - 💾 Tentando salvar no banco de dados...
2026-03-03T17:29:48.2385425Z 2026-03-03 17:29:48,236 - sqlalchemy.engine.Engine - INFO - BEGIN (implicit)

🎯 WEBHOOK JOTFORM RECEBIDO
2026-03-03T17:28:20.600475Z 2026-03-03 17:28:20,600 - api.webhook - INFO - ================================================================================
2026-03-03T17:28:20.6004764Z 2026-03-03 17:28:20,600 - api.webhook - INFO - 📋 Headers recebidos:
2026-03-03T17:28:20.6004779Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    accept: */*
2026-03-03T17:28:20.6004795Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    host: webhook-stone.azurewebsites.net
2026-03-03T17:28:20.6006204Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    max-forwards: 10
2026-03-03T17:28:20.6006331Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    traceparent: 00-0000000000000000bde96176573b79b6-3d90399712da838e-01
2026-03-03T17:28:20.6006384Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    tracestate: 2849407@nr=0-0-2849407-547973083-3d90399712da838e-bde96176573b79b6-1-1.553159-1772558900530
2026-03-03T17:28:20.6006416Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    newrelic: eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkFwcCIsImFjIjoiMjg0OTQwNyIsImFwIjoiNTQ3OTczMDgzIiwiaWQiOiIzZDkwMzk5NzEyZGE4MzhlIiwidHIiOiJiZGU5NjE3NjU3M2I3OWI2IiwidHgiOiJiZGU5NjE3NjU3M2I3OWI2IiwicHIiOjEuNTUzMTYsInNhIjp0cnVlLCJ0aSI6MTc3MjU1ODkwMDUzMH19
2026-03-03T17:28:20.6006437Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-arr-log-id: 44e0d3a0-d567-4b67-8843-7f701f09a644
2026-03-03T17:28:20.6006456Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    client-ip: 35.203.6.156:41928
2026-03-03T17:28:20.6007214Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    disguised-host: webhook-stone.azurewebsites.net
2026-03-03T17:28:20.600726Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-site-deployment-id: webhook-stone
2026-03-03T17:28:20.6007279Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    was-default-hostname: webhook-stone.azurewebsites.net
2026-03-03T17:28:20.6007338Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-forwarded-proto: https
2026-03-03T17:28:20.6008171Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-appservice-proto: https
2026-03-03T17:28:20.6008321Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-arr-ssl: 2048|256|CN=Microsoft Azure RSA TLS Issuing CA 04, O=Microsoft Corporation, C=US|CN=*.azurewebsites.net, O=Microsoft Corporation, L=Redmond, S=WA, C=US
2026-03-03T17:28:20.6008343Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-forwarded-tlsversion: 1.3
2026-03-03T17:28:20.6008542Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-forwarded-for: 35.203.6.156:41928
2026-03-03T17:28:20.600859Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-original-url: /api/v1/webhook/jotform
2026-03-03T17:28:20.6008653Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-waws-unencoded-url: /api/v1/webhook/jotform
2026-03-03T17:28:20.6009205Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-client-ip: 35.203.6.156
2026-03-03T17:28:20.6009242Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    x-client-port: 41928
2026-03-03T17:28:20.6009509Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    content-type: multipart/form-data; boundary=------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6009921Z 2026-03-03 17:28:20,600 - api.webhook - INFO -    content-length: 4915
2026-03-03T17:28:20.601126Z 2026-03-03 17:28:20,600 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:28:20.6016357Z 2026-03-03 17:28:20,601 - api.webhook - INFO - 📦 Body bruto (tamanho: 4890 bytes):
2026-03-03T17:28:20.6016549Z 2026-03-03 17:28:20,601 - api.webhook - INFO - --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016568Z Content-Disposition: form-data; name="action"
2026-03-03T17:28:20.6016582Z
2026-03-03T17:28:20.6016594Z
2026-03-03T17:28:20.6016609Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016624Z Content-Disposition: form-data; name="webhookURL"
2026-03-03T17:28:20.6016636Z
2026-03-03T17:28:20.6016651Z https://webhook-stone.azurewebsites.net/api/v1/webhook/jotform
2026-03-03T17:28:20.6016668Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016683Z Content-Disposition: form-data; name="username"
2026-03-03T17:28:20.6016715Z
2026-03-03T17:28:20.6016729Z !team_260064573416051
2026-03-03T17:28:20.6016743Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016758Z Content-Disposition: form-data; name="formID"
2026-03-03T17:28:20.601677Z
2026-03-03T17:28:20.6016783Z 253594218352056
2026-03-03T17:28:20.6016799Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016813Z Content-Disposition: form-data; name="type"
2026-03-03T17:28:20.6016826Z
2026-03-03T17:28:20.6016839Z WEB
2026-03-03T17:28:20.6016853Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016867Z Content-Disposition: form-data; name="customParams"
2026-03-03T17:28:20.6016897Z
2026-03-03T17:28:20.6016909Z
2026-03-03T17:28:20.6016929Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016944Z Content-Disposition: form-data; name="product"
2026-03-03T17:28:20.6016957Z
2026-03-03T17:28:20.6016969Z
2026-03-03T17:28:20.6016983Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6016996Z Content-Disposition: form-data; name="formTitle"
2026-03-03T17:28:20.6017008Z
2026-03-03T17:28:20.6017025Z Formulário de Inscrição
2026-03-03T17:28:20.601704Z --------------------------D9r4pLklrB5ZQnHXan2jEx
2026-03-03T17:28:20.6017053Z Cont
2026-03-03T17:28:20.601712Z 2026-03-03 17:28:20,601 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:28:20.6061044Z 2026-03-03 17:28:20,601 - api.webhook - WARNING - ⚠️ Body não é JSON válido: Expecting value: line 1 column 1 (char 0)
2026-03-03T17:28:20.6061135Z 2026-03-03 17:28:20,601 - api.webhook - INFO - 🔄 Tentando parsear como form-data...
2026-03-03T17:28:20.6100342Z 2026-03-03 17:28:20,609 - api.webhook - INFO - ✅ Body parseado como form-data com sucesso
2026-03-03T17:28:20.6100571Z 2026-03-03 17:28:20,609 - api.webhook - INFO - 📥 Payload parseado:
2026-03-03T17:28:20.6101799Z 2026-03-03 17:28:20,610 - api.webhook - INFO - {
2026-03-03T17:28:20.6101839Z   "action": "",
2026-03-03T17:28:20.6101859Z   "webhookURL": "https://webhook-stone.azurewebsites.net/api/v1/webhook/jotform",
2026-03-03T17:28:20.6101874Z   "username": "!team_260064573416051",
2026-03-03T17:28:20.6101888Z   "formID": "253594218352056",
2026-03-03T17:28:20.6101902Z   "type": "WEB",
2026-03-03T17:28:20.6101935Z   "customParams": "",
2026-03-03T17:28:20.6101951Z   "product": "",
2026-03-03T17:28:20.6101969Z   "formTitle": "Formulário de Inscrição",
2026-03-03T17:28:20.6101984Z   "customTitle": "",
2026-03-03T17:28:20.6102001Z   "submissionID": "6483680996011996615",
2026-03-03T17:28:20.6102014Z   "event": "",
2026-03-03T17:28:20.6102027Z   "documentID": "",
2026-03-03T17:28:20.610204Z   "teamID": "",
2026-03-03T17:28:20.6102053Z   "subject": "",
2026-03-03T17:28:20.6102067Z   "isSilent": "",
2026-03-03T17:28:20.6102079Z   "customBody": "",
2026-03-03T17:28:20.6102186Z   "rawRequest": "{\"slug\":\"submit\\/253594218352056\",\"uploadServerUrl\":\"https:\\/\\/freehelper.jotform.com\\/upload\",\"jsExecutionTracker\":\"build-date-1772558705337=>init-started:1772558762202=>validator-called:1772558762300=>validator-mounted-false:1772558762303=>init-complete:1772558762368=>interval-complete:1772558783358=>observerSubmitHandler_received-submit-event:1772558898357=>submit-validation-passed:1772558898753=>observerSubmitHandler_validation-passed-submitting-form:1772558898915\",\"submitSource\":\"form\",\"submitDate\":\"1772558898915\",\"buildDate\":\"1772558705337\",\"q6_nomeCompleto6\":{\"first\":\"Tallita\",\"last\":\"silva\"},\"q7_email7\":\"tallitaantoniasilva@gmail.com\",\"q8_telefonecom\":{\"area\":\"55\",\"phone\":\"+5562999857200\"},\"q9_cpf\":\"06437743190\",\"q10_voceVeio\":[\"N\\u00e3o, n\\u00e3o vim de nenhuma organiza\\u00e7\\u00e3o da Rede Instituto Stone.\"],\"q14_cidade\":\"S\\u00e3o Jo\\u00e3o D'Alian\\u00e7a \",\"q16_estado\":\"Goi\\u00e1s\",\"q17_idade\":\"25 a 34 anos\",\"q18_genero\":\"Feminino\",\"q19_escolaridade\":\"Ensino Superior Incompleto\",\"q20_faixaDe\":\"Entre 2 e 3 sal\\u00e1rios m\\u00ednimos\",\"q22_tempoDe\":\"6 meses a 1 ano\",\"q23_segmentoDe\":\"Outros\",\"q25_consentimentoPara\":\"Aceito\",\"q26_declaroQue\":\"Sim\",\"newCardFormMobile\":\"1\",\"event_id\":\"1772558762204_253594218352056_crQEKMq\",\"timeToSubmit\":\"20\",\"enterprise_server\":\"freehelper.jotform.com\",\"validatedNewRequiredFieldIDs\":\"{\\\"new\\\":1,\\\"id_6\\\":\\\"si\\\",\\\"id_7\\\":\\\"ta\\\",\\\"id_8\\\":\\\"+5\\\",\\\"id_9\\\":\\\"06\\\",\\\"id_10\\\":\\\"N\\u00e3\\\",\\\"id_14\\\":\\\"S\\u00e3\\\",\\\"id_16\\\":\\\"To\\\",\\\"id_17\\\":\\\"Ac\\\",\\\"id_18\\\":\\\"Pr\\\",\\\"id_19\\\":\\\"Do\\\",\\\"id_20\\\":\\\"Ac\\\",\\\"id_22\\\":\\\"Ma\\\",\\\"id_25\\\":\\\"Ac\\\",\\\"id_26\\\":\\\"Si\\\"}\",\"path\":\"\\/submit\\/253594218352056\"}",
2026-03-03T17:28:20.6102203Z   "fromTable": "",
2026-03-03T17:28:20.6102215Z   "appID": "",
2026-03-03T17:28:20.6102268Z   "pretty": "Nome completo::Tallita silva, E-mail::tallitaantoniasilva@gmail.com, Telefone (com DDD)::55 +5562999857200, CPF::06437743190, Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?:Não, não vim de nenhuma organização da Rede Instituto Stone., Cidade::São João D'Aliança , Estado::Goiás, Idade::25 a 34 anos, Gênero::Feminino, Escolaridade::Ensino Superior Incompleto, Faixa de Renda Familiar Mensal::Entre 2 e 3 salários mínimos, Tempo de funcionamento do negócio::6 meses a 1 ano, Segmento de atuação::Outros, Consentimento para uso de dados pessoais.:Aceito, Declaro que todas as informações fornecidas são verdadeiras e estou ciente das condições do programa.:Sim",
2026-03-03T17:28:20.6102282Z   "unread": "",
2026-03-03T17:28:20.6102313Z   "parent": "",
2026-03-03T17:28:20.6102328Z   "ip": "168.228.215.106"
2026-03-03T17:28:20.6102341Z }
2026-03-03T17:28:20.610236Z 2026-03-03 17:28:20,610 - api.webhook - INFO - ================================================================================
2026-03-03T17:28:20.6109388Z 2026-03-03 17:28:20,610 - api.webhook - INFO - 🔄 Detectado formato form-data do Jotform com rawRequest
2026-03-03T17:28:20.6109539Z 2026-03-03 17:28:20,610 - api.webhook - INFO - 📋 Metadados: formID=253594218352056, submissionID=6483680996011996615
2026-03-03T17:28:20.6109562Z 2026-03-03 17:28:20,610 - api.webhook - INFO - ✅ rawRequest parseado com sucesso
2026-03-03T17:28:20.610958Z 2026-03-03 17:28:20,610 - api.webhook - INFO - ✅ Campos mapeados com sucesso
2026-03-03T17:28:20.6109599Z 2026-03-03 17:28:20,610 - api.webhook - INFO - 📦 Payload mapeado:
2026-03-03T17:28:20.6109614Z 2026-03-03 17:28:20,610 - api.webhook - INFO - {
2026-03-03T17:28:20.6109649Z   "Nome": {
2026-03-03T17:28:20.6109663Z     "first": "Tallita",
2026-03-03T17:28:20.6109678Z     "last": "silva"
2026-03-03T17:28:20.6109691Z   },
2026-03-03T17:28:20.6109706Z   "E-mail": "tallitaantoniasilva@gmail.com",
2026-03-03T17:28:20.610972Z   "Telefone": {
2026-03-03T17:28:20.6109733Z     "area": "55",
2026-03-03T17:28:20.6109746Z     "phone": "+5562999857200"
2026-03-03T17:28:20.6109759Z   },
2026-03-03T17:28:20.6109773Z   "CPF": "06437743190",
2026-03-03T17:28:20.6109797Z   "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Não, não vim de nenhuma organização da Rede Instituto Stone.",
2026-03-03T17:28:20.6109828Z   "Cidade": "São João D'Aliança ",
2026-03-03T17:28:20.6109845Z   "Estado": "Goiás",
2026-03-03T17:28:20.6109859Z   "Idade": "25 a 34 anos",
2026-03-03T17:28:20.6109874Z   "Gênero": "Feminino",
2026-03-03T17:28:20.6109889Z   "Escolaridade": "Ensino Superior Incompleto",
2026-03-03T17:28:20.6109905Z   "Faixa de renda familiar mensal": "Entre 2 e 3 salários mínimos",
2026-03-03T17:28:20.6109921Z   "Tempo de funcionamento do negócio": "6 meses a 1 ano",
2026-03-03T17:28:20.6109939Z   "Segmento de atuação": "Outros",
2026-03-03T17:28:20.6109955Z   "submissionID": "6483680996011996615",
2026-03-03T17:28:20.6109969Z   "formID": "253594218352056"
2026-03-03T17:28:20.6109981Z }
2026-03-03T17:28:20.6109998Z 2026-03-03 17:28:20,610 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:28:20.6110037Z 2026-03-03 17:28:20,610 - api.webhook - INFO - 📦 Payload final para processar:
2026-03-03T17:28:20.6110052Z 2026-03-03 17:28:20,610 - api.webhook - INFO - {
2026-03-03T17:28:20.6110065Z   "Nome": {
2026-03-03T17:28:20.6110079Z     "first": "Tallita",
2026-03-03T17:28:20.6110095Z     "last": "silva"
2026-03-03T17:28:20.6110107Z   },
2026-03-03T17:28:20.6110121Z   "E-mail": "tallitaantoniasilva@gmail.com",
2026-03-03T17:28:20.6110134Z   "Telefone": {
2026-03-03T17:28:20.6110147Z     "area": "55",
2026-03-03T17:28:20.6110162Z     "phone": "+5562999857200"
2026-03-03T17:28:20.6110175Z   },
2026-03-03T17:28:20.6110208Z   "CPF": "06437743190",
2026-03-03T17:28:20.6110235Z   "Você veio de alguma organização da Rede Instituto Stone? Se sim, qual?": "Não, não vim de nenhuma organização da Rede Instituto Stone.",
2026-03-03T17:28:20.611025Z   "Cidade": "São João D'Aliança ",
2026-03-03T17:28:20.6110263Z   "Estado": "Goiás",
2026-03-03T17:28:20.6110277Z   "Idade": "25 a 34 anos",
2026-03-03T17:28:20.6110291Z   "Gênero": "Feminino",
2026-03-03T17:28:20.6110306Z   "Escolaridade": "Ensino Superior Incompleto",
2026-03-03T17:28:20.6110324Z   "Faixa de renda familiar mensal": "Entre 2 e 3 salários mínimos",
2026-03-03T17:28:20.6110339Z   "Tempo de funcionamento do negócio": "6 meses a 1 ano",
2026-03-03T17:28:20.6110354Z   "Segmento de atuação": "Outros",
2026-03-03T17:28:20.6110368Z   "submissionID": "6483680996011996615",
2026-03-03T17:28:20.6110401Z   "formID": "253594218352056"
2026-03-03T17:28:20.6110414Z }
2026-03-03T17:28:20.6110431Z 2026-03-03 17:28:20,610 - api.webhook - INFO - --------------------------------------------------------------------------------
2026-03-03T17:28:20.6110453Z 2026-03-03 17:28:20,610 - api.webhook - INFO - ✅ Payload validado com sucesso
2026-03-03T17:28:20.6110546Z 2026-03-03 17:28:20,610 - api.webhook - INFO - ✅ Dados processados: Nome=Tallita silva, Telefone=(55) +5562999857200