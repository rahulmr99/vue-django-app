(function () {
    var companyID = '{{ company_id }}';
    var domainName = '{{ domain_name }}';

    // function loadCss(file) {
    //     var link = document.createElement('link')
    //     link.href = file
    //     link.type = 'text/css'
    //     link.rel = 'stylesheet'
    //     link.media = 'screen,print'
    //     document.getElementsByTagName('head')[0].appendChild(link)
    // }

    var createEmbedElement = function () {
        var elem = document.createElement('iframe');
        elem.setAttribute("src", domainName + '/embedded/' + companyID);
        elem.setAttribute("frameborder", "0");
        elem.setAttribute("id", "embed-booking-page");
        elem.setAttribute("width", "100%");
        elem.setAttribute("height", "830px");
        return elem;
    };
    var modal = document.createElement('div');
    modal.classList = ['popup-modal'];
    var embedElement = createEmbedElement();
    var modalContent = document.createElement('div');
    modalContent.classList = ['popup-modal-content'];
    modalContent.appendChild(embedElement);

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

// add element click listener
    var clickHandler = function (event) {
        event.preventDefault();
        modal.style.display = 'block'
    };
    var button = document.getElementById('easy-booking-btn-styled');
    if (button) {
        // create default button here if not available in page
        button.onclick = clickHandler
    }
    var els = document.querySelectorAll('a[href^=\'https://secure.bookedfusion.com/\']');
    var aBookLink;
    if (els.length > 0) {
        // If there are more than one booking link need to add then attach 
        // click event to all of the <a></a> tag
        for(let i=0;i<els.length;i++){
            aBookLink = els[i];
            aBookLink.onclick = clickHandler
        }
    }
    if (!(aBookLink || button)) {
        console.log('iframe is not configured correctly')
    }

    // event listeners
    window.addEventListener('message', function (event) {
        if (event.data === 'closeModalDlg') {
            modal.style.display = 'none'
        }
    }, true)
})();