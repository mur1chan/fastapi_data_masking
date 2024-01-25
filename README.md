# Data Masking Software
## Überblick 
Data Masking ist ein modernes Softwareprojekt, das darauf abzielt, sensible Daten durch Pseudonymisierung und Anonymisierung zu schützen. 
Dieses Projekt bietet robuste Sicherheitsmechanismen für Benutzerauthentifizierung und Datenhandling, wobei es auf modernen Webtechnologien und Sicherheitsstandards basiert. 

### Benutzerauthentifizierung:
- Sichere Authentifizierung mittels OAuth2.
- JWTs für Benutzersicherheit und
- verwaltung.
### Pseudonymisierung von Daten:
  - Fähigkeit zur sicheren Pseudonymisierung sensibler Daten.
  -  Unterstützung für Passwort-basierte Datenverschlüsselung.
### Rückgängigmachung der Pseudonymisierung:
- Möglichkeit zur sicheren Dekodierung pseudonymisierter Daten.
### Anonymisierung von Daten:
- Vollständige Anonymisierung von Daten mittels SHA-256 Hashing.
### Sicherheitskonformität:
- Übereinstimmung mit aktuellen Sicherheitsstandards.
- Einhaltung von Datenschutzgesetzen.
### Dockerfile:
- PASSWORD ist ein Hash für die Kombination von Nutzername und Passwort.
- PASSWORDSTR ist das Passwort der Kombination als Text, um es dem Nutzernamen bei der Entschlüsselung zuzuordnen.
Code für die Generierung von PASSWORD:
```
import rncryptor
cryptor = rncryptor.RNCryptor()
password = cryptor.encrypt("username", "password").hex()
```
## Lizenz
Dieses Projekt steht unter einer spezifischen Lizenz. Details finden Sie in der Datei `LICENSE`.
