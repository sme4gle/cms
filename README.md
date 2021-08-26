# Demo CMS app

Over het CMS; Ik heb gekozen om de app te bouwen in Flask.
De frontend word gerenderd met behulp van Jinja2.
Al het database verkeerd word geregeld door SqlAlchemy en PsychoPg. In mijn geval heb ik deze geconfigureerd om te praten met een PostgreSQL 13 server. Maar in theorie zou dit ook moeten werken met bijv. MySQL.

### Hoe zet ik de applicatie op?
1. Zet een database op, de applicatie is geconfigureerd voor een database met de naam 'cmsdemo' en gebruiker 'cmsdemo' **zonder** wachtwoord.
2. Installeer de benodigde libraries. Ik heb ze in handig formaat in "requirements.txt" file gezet. Draai in de root van de applicatie het commando **pip install -r requirements.txt**
3. Om de applicatie te laten werken moeten we de database even bijwerken. Dit kunnen we doen door in de root folder even **flask db upgrade** uit te voeren. Hierdoor voert Alembic automatisch de migratiescriptjes uit.
4. Start de app.
5. Pak een bak koffie, You earned it! Nu kun je als het goed is mijn app bekijken op https://localhost:5000 


### Login info
* Er bestaat al een admin user, met de originele username *admin*. Het wachtwoord van dit account is *24augustus*
* Er bestaat ook al een author user, met  de username *author* en wachtwoord *test123*

Als het goed is kan de admin account posts maken, editten en posts verwijderen. Het author account kan dit  ook, alleen heeft dit account alleen de rechten om dat te doen voor de posts die het account zelf geplaatst heeft.

De applicatie is verre van perfect, en heeft hier en daar nog wat gekke quirks.
Als ik er wat meer tijd aan had besteed dan de voorgeschreven twee dagdelen zou ik op diverse plekken wat betere foutafhandeling hebben geïmplementeerd.
Verder zou ik de tests wat hebben uitgebreid zodat de coverage wat omhoog gaat.
