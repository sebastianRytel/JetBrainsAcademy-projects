<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
<div class="title">Case Converter</div>
<div>
    <textarea rows="5" cols ="33">
    </textarea>
</div>
<div>
    <button id="upper-case">Upper Case</button>
    <button id="lower-case">Lower Case</button>
    <button id="proper-case">Proper Case</button>
    <button id="sentence-case">Sentence Case</button>
    <button id="save-text-file">Save Text File</button>
</div>
<script>
    document.getElementById("upper-case").addEventListener("click", function() {
            let words = document.querySelector("textarea").value;
            document.querySelector("textarea").value = words.toUpperCase();
        }
    )
    document.getElementById("lower-case").addEventListener("click", function() {
            let words = document.querySelector("textarea").value;
            document.querySelector("textarea").value = words.toLowerCase();
        }
    )
    document.getElementById("proper-case").addEventListener("click", function() {
            let words = document.querySelector("textarea").value;
            let splitSentence = words.split(" ")
            let properCased = splitSentence.map((word) => {
                return word[0].toUpperCase() + word.slice(1)
            })
            document.querySelector("textarea").value = properCased.join(' ');
        }
    )
    document.getElementById("sentence-case").addEventListener("click", function() {
        let words = document.querySelector("textarea").value;
        let lowerCaseWords = words.toLowerCase();
        let splitSentence = lowerCaseWords.split(". ")

        let sentenceCase = splitSentence.map((word) => {
            return word[0].toUpperCase() + word.slice(1)
        })

            document.querySelector("textarea").value = sentenceCase.join('. ');
        })

    function download(filename, text) {
        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

    document.getElementById("save-text-file").addEventListener("click", function () {
        let textToBeSaved = document.querySelector("textarea").value;
        download("text.txt", textToBeSaved);
    })



</script>
</body>
</html>
