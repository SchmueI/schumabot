# schumabot

## Über Schulmanager-Online
Schulmanager Online ist eine Plattform, welche den Schulalltag von inzwischen über 2.400 Schulen digitalisiert und dadurch einen großen (positiven!) Einfluss auf die Zugänglichkeit von tagesaktuellen Informationen nimmt. Diese Arbeit zeichnet sich durch das Vorhandensein einer eigenen Website sowie Apps für iOS und Android aus.

Einige Anwender der hunderten Schulen verwenden allerdings nur ungern die Web- Anwendung; besitzen kein Android oder iOS Mobilgerät; oder haben ganz andere, persönliche Gründe, nach einem weiteren Zugangspunkt zu suchen. Eine Möglichkeit hierfür stellt der Schuma bot dar. Die zugrundeliegende API verwendet die quelloffene Bibliothek Selenium zur Browser-Automatisierung und wird derzeit von der Schulmanager Online GmbH, welche die Plattform zur Verfügung stellt und entwickelt, wohlwollend geduldet.

## Über den Bot
Der Schumabot verwendet Telegram als Kommunikationsplattform für die Weiterleitung von Informationen. Das Prinzip ist denkbar einfach. Der Nutzer führt die Web-Aufrufe nicht mehr mit einem Browser, sondern remote mit dem Browser des Host-Systems des Bots aus. In diesem Fall wird Chrome eingesetzt. Zur Ermittlung der für den Nutzer verfügbaren Daten verwendet der Bot die zuvor hinterlegten Zugangsdaten. Dringend sei empfohlen, als Bot-Betreiber hinsichtlich der Speicherung und Verwaltung der Daten ein sicheres System zu verwenden und die Nutzer im Rahmen einer Datenschutzerklärung darüber aufzuklären, welche Risiken eine Third-Party-API mit sich bringt.
