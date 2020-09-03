let references = []

function populateReferences() {
    let localReferences = document.querySelector('div.references');
    if (localReferences) {
        let liReferences = localReferences.querySelector('ol').querySelectorAll('li');
        references = [...liReferences]
    }
}

function handleReferenceClick() {
    let content = this.textContent.trim();
    let referenceNumber = parseInt(content.slice(1, -1)) - 1;
    if (referenceNumber >= references.length) {
        return;
    }
    references[referenceNumber].scrollIntoView({behavior: 'smooth', block: 'center'});
}

function addReferenceHandlers() {
    let referenceClasses = ["span.reference", "span.sup-reference"];
    for (let ri = 0; ri < referenceClasses.length; ri++) {
        let spanReferences = document.querySelectorAll(referenceClasses[ri]);
        for (let i = 0; i < spanReferences.length; i++) {
            spanReferences[i].onclick = handleReferenceClick;
        }
    }
}

function addTagLinks() {
    let tags = document.querySelector('ul.taglist').querySelectorAll('li');
    for (let i = 0; i < tags.length; i++) {
        let tag = tags[i];
        let a = tag.querySelector('a');
        if (a) {
            a.href = "/tag/" + a.textContent.trim().toLowerCase() + ".html";
        }
    }
}

// TODO: Move this TOC building to generate.py
function fillSubSectionInTOC(sectionElement, sectionId, subSections) {
    if (subSections.length == 0) {
        return;
    }

    let subSectionList = document.createElement("ul");
    subSectionList.classList.add("subsectionlist");
    for (let i = 1; i <= subSections.length; i++) {
        let subSection = subSections[i - 1];
        subSection.id = "section-" + sectionId.toString() + "-" + i.toString();

        let subSectionElement = document.createElement("li");
        let subSectionText = document.createElement("span");
        subSectionText.innerHTML = subSection.textContent.trim();
        subSectionText.classList.add("link");
        subSectionText.onclick = function() {
            subSection.scrollIntoView({behavior: 'smooth', block: 'center'});
        }
        subSectionElement.appendChild(subSectionText);
        subSectionList.appendChild(subSectionElement);
    }

    sectionElement.appendChild(subSectionList);
}

function fillSectionInTOC(sectionList, sectionId, section) {
    section.id = "section-" + sectionId.toString();
    let sectionTitle = section.querySelector('h3.section-title');

    let sectionElement = document.createElement("li");
    let sectionText = document.createElement("span");
    sectionText.innerHTML = sectionTitle.textContent.trim();
    sectionText.classList.add("link")
    sectionText.onclick = function() {
        sectionTitle.scrollIntoView({behavior: 'smooth', block: 'center'});
    }
    sectionElement.appendChild(sectionText);

    let subSections = section.querySelectorAll('h4');
    fillSubSectionInTOC(sectionElement, sectionId, subSections);

    sectionList.appendChild(sectionElement);
}

function fillTOC() {
    let toc = document.getElementById('toc');
    if (!toc) {
        return;
    }

    let sections = document.querySelectorAll('.section');

    let tocHeading = document.createElement("h3");
    tocHeading.innerHTML = "Table of Contents";
    toc.appendChild(tocHeading);

    let sectionList = document.createElement("ol");
    sectionList.classList.add("sectionlist");
    for (let sectionId = 1; sectionId <= sections.length; sectionId++) {
        fillSectionInTOC(sectionList, sectionId, sections[sectionId - 1]);
    }

    toc.appendChild(sectionList);
}

populateReferences();
addReferenceHandlers();
addTagLinks();
fillTOC();

