<h1>Anki automatic english vocabulary adding script.</h1>
<p>Uses google translate for audio and open dictionary API for definitions. Written in Python, uses Ankiconnect API to interface with Anki. </p>

<h2>Usage</h2>
<ol>
<li>Create text file in the same location with all the words you wish to add</li>
<li>Add the file name to the script and change the default separator if wanted (default is a newline) </li>
<li>Modify the note settings to match that of your desired deck and fields.</li>
<li>Run </li>
</ol>

<p>The script automatically creates a textfile called "logs" which contains all the words added and their ids if sucessful, or "None" if not added. By default, missing parameters default to the note not being added. Also adds a flag depending on which request (audio or glossary) failed. Import the collection i added if you wish the same vocab card i used. </p>