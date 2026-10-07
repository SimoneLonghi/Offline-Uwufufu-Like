# Offline Uwufufu-Like Tournament

A desktop tournament app built with Python, PyQt6, and Qt WebEngine. It loads contestants from an Excel workbook, displays their links side by side, and records the winner of each group to create the next tournament round.

- Load an `.xlsx` workbook without modifying the source file.
- Compare contestants in a group using their links in embedded browser views.
- For groups with more than two contestants, use a **King of the Hill** format: the current champion faces each remaining contestant in order.
- A group with one contestant advances automatically.
- Save generated workbooks and tournament progress in an `output` directory beside the script or packaged executable.
- Use the in-app exit button during a tournament to save progress before closing.
- At the end of each round, the app writes a new `.xlsx` workbook containing the group winners. That workbook is used to start the next round; after the final round, the app displays the winner.
- Progress is saved after each completed group in Excel workbook.

The worksheet must contain a header row with these columns (header matching is case-insensitive): NOME, LINK, GIRONE.