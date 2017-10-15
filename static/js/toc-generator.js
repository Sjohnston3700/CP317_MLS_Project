/*
 * Dynamic Table of Contents script
 * By Matt Whitlock <http://www.whitsoftdev.com/>, edited by Sumeet Jhand
 * Usage: Table of Contents heading must be in a div named "toc".
		  Create headings as you normally would. Don't include the section number. Script handles that.
		  Any heading you don't want in the TOC must be in a div named "toc_exclude".
 */

function createLink(href, innerHTML) {
	var a = document.createElement("a");
	a.setAttribute("href", href);
	a.innerHTML = innerHTML;
	return a;
}

window.onload = function() {
	var i2 = 0,
		i3 = 0,
		i4 = 0,
		i5 = 0;
	toc = toc.appendChild(document.createElement("ul"));
	for (var i = 0; i < document.body.childNodes.length; ++i) {
		var node = document.body.childNodes[i];
		var tagName = node.nodeName.toLowerCase();
		if (node.id != "toc_exclude") {
			if (tagName == "h5") {
				++i5;
				if (i5 == 1) toc.lastChild.lastChild.lastChild.lastChild.lastChild.appendChild(document.createElement("ul"));
				var section = i2 + "." + i3 + "." + i4 + "." + i5;
				node.insertBefore(document.createTextNode(section + ". "), node.firstChild);
				node.id = "section" + section;
				toc.lastChild.lastChild.lastChild.lastChild.lastChild.lastChild.appendChild(document.createElement("li")).appendChild(createLink("#section" + section, node.innerHTML));
			} else if (tagName == "h4") {
				++i4;
				if (i4 == 1) toc.lastChild.lastChild.lastChild.appendChild(document.createElement("ul"));
				var section = i2 + "." + i3 + "." + i4;
				node.insertBefore(document.createTextNode(section + ". "), node.firstChild);
				node.id = "section" + section;
				toc.lastChild.lastChild.lastChild.lastChild.appendChild(document.createElement("li")).appendChild(createLink("#section" + section, node.innerHTML));
			} else if (tagName == "h3") {
				++i3, i4 = 0;
				if (i3 == 1) toc.lastChild.appendChild(document.createElement("ul"));
				var section = i2 + "." + i3;
				node.insertBefore(document.createTextNode(section + ". "), node.firstChild);
				node.id = "section" + section;
				toc.lastChild.lastChild.appendChild(document.createElement("li")).appendChild(createLink("#section" + section, node.innerHTML));
			} else if (tagName == "h2") {
				++i2, i3 = 0, i4 = 0;
				var section = i2;
				node.insertBefore(document.createTextNode(section + ". "), node.firstChild);
				node.id = "section" + section;
				toc.appendChild(h2item = document.createElement("li")).appendChild(createLink("#section" + section, node.innerHTML));
			}
		}
	}
};