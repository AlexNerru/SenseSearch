listOFLinks = [];

Dropzone.options.myAwesomeDropzone = {
    maxFilesize: 20, // Size in MB
    dictDefaultMessage: "Перенесите файлы сюда или кликните для загрузки",
    previewsContainer: false,
    removedfile: function (file) {
        var fileRef;
        return (fileRef = file.previewElement) != null ?
            fileRef.parentNode.removeChild(file.previewElement) : void 0;
    },

    success: function (file, response) {
        createZone();
        createCardLinkArea();
        createNewCard(file, response);
    },

    error: function (file, response) {
        alert(response);
    }

};

function createZone() {
    var div = document.createElement('div');
    div.className = 'card';
    div.id = 'cardZone';
    cardZone = document.getElementById("cards");
    cardZone.appendChild(div);

}

function createCardLinkArea() {

    var div = document.createElement('div');
    div.className = 'list-group list-group-flush';
    div.id = "cardList";
    cardLinks = document.getElementById("cardZone");
    cardLinks.appendChild(div);

}

function createLinkBlock(label, link, id, className) {
    var div = document.createElement('div');
    div.className = 'block';

    var input = document.createElement('input');
    input.className = 'link-input form-control';
    input.value = link;
    input.id = id;

    var linkLabel = document.createElement("label");
    linkLabel.for = 'id';
    linkLabel.innerHTML = label;
    linkLabel.className = className;

    div.appendChild(linkLabel);
    div.appendChild(input);
    return div;
}

function createNewCard(file, response) {
    var data = JSON.parse(response);

    var img = document.createElement('img');
    img.className = 'img-responsive';
    img.id = 'img';
    img.src = file.dataURL;

    var directLink = createLinkBlock('Прямая сслыка:', data.direct, 'directLink', 'link');
    var markdownLink = createLinkBlock('Markdown:', data.markdown, 'markdownLink', 'link');
    var htmlLink = createLinkBlock('HTML:', data.html, 'htmlLink', 'link');
    var insideDiv = document.createElement('div');
    insideDiv.appendChild(directLink);
    insideDiv.appendChild(markdownLink);
    insideDiv.appendChild(htmlLink);

    var div = document.createElement('div');
    div.className = 'list-group-item';
    div.id = 'list-group-item';

    var row = document.createElement('div');
    row.className = 'row';

    var leftColumn = document.createElement('div');
    leftColumn.className = 'col-md-3';

    var rightColumn = document.createElement('div');
    rightColumn.className = 'col-md-9';
    rightColumn.id = 'rightColumn';

    var formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    formGroup.appendChild(insideDiv);

    leftColumn.appendChild(img);
    rightColumn.appendChild(formGroup);
    row.appendChild(leftColumn);
    row.appendChild(rightColumn);
    div.appendChild(row);
    cardList = document.getElementById("cardList");
    cardList.appendChild(div);
}




