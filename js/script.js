let references = []

function populateReferences() {
    let localReferences = document.querySelector('div.references');
    if (localReferences) {
        let liReferences = localReferences.querySelector('ol').querySelectorAll('li');
        references = [...liReferences]
    }
}

function handleReferenceClick() {
    referenceNumber = parseInt(this.textContent[1]);
    if (referenceNumber >= references.length) {
        return;
    }
    references[referenceNumber].scrollIntoView({behavior: 'smooth', block: 'center'});
}

function addTagLinks() {
    let tags = document.querySelector('ul.taglist').querySelectorAll('li');
    for (let i = 0; i < tags.length; i++) {
        let tag = tags[i];
        let a = tag.querySelector('a');
        if (a) {
            a.href = "/tag/" + a.textContent.toLowerCase() + ".html";
        }
    }
}

function setupSections() {
    let sections = document.querySelectorAll('.section');
    for (let i = 0; i < sections.length; i++) {
        sections[i].classList.add('mt-5');
    }
}

populateReferences();
let spanReferences = document.querySelectorAll('span.reference');
for (let i = 0; i < spanReferences.length; i++) {
    spanReferences[i].onclick = handleReferenceClick;
}

addTagLinks();

setupSections();
