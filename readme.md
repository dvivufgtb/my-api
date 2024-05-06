# API
<h2> String Manipulation</h2>
<h3><details><summary>/regex (POST)</summary>
<h4> Request body</h4>
<button aria-controls="SMeeaRU=" aria-selected="true" class="tablinks" data-name="example" id="3WgPHEk=" role="tab">Example Value</button><br>
<h5><pre>{
 "regex" : "[A-Z]+",
 "text": "MANYAK"
}</pre></h5></h4></details></h3>
<h3><details><summary>/split (POST)</summary>

<h4> Request body</h4>
<button aria-controls="SMeeaRU=" aria-selected="true" class="tablinks" data-name="example" id="3WgPHEk=" role="tab">Example Value</button><br>
<h5><pre>{
 "sep" : " ",
 "text": "your text here"
}</pre></h5></h4></details></h3>
<h3><details><summary>/random (POST)</summary>
<h4> Request body</h4>
<button aria-controls="SMeeaRU=" aria-selected="true" class="tablinks" data-name="example" id="3WgPHEk=" role="tab">Example Value</button><br>
<h5><pre>{
 "choices":"0123456789",
 "amount": 6
}</pre></h5></h4></details></h3>
<h3><details><summary>/base64 (POST)</summary>
<h4> Query</h4>
<b>encode</b> - if argument is false, it will decode from base64
<h4> Request body</h4>
<button aria-controls="SMeeaRU=" aria-selected="true" class="tablinks" data-name="example" id="3WgPHEk=" role="tab">Example Value</button><br>
<h5><pre>{
 "value": "your_text"
}</pre></h5></h4></details></h3>
<h2>Time</h2>
<h3><details><summary>/isoformat/&lt;unix&gt; (GET)</summary></details></h3>
<h2>Discord</h2>
<h3><details><summary>/discord-permissions/&lt;int&gt; (GET)</summary></details></h3>
