{% load staticfiles %}

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

function addParam(e, n, t) {
    return t && void 0 != t && "undefined" != t ? e + (e.indexOf("?") >= 0 ? "&" : "?") + n + "=" + t : e
}
function buildURL(e,n) {
    var t = e;
    for (var o in n) n.hasOwnProperty(o) && (t = addParam(t, o, n[o]));
    return t
}
function showBox(customer){
    document.getElementById("box").classList.remove("hide");
    var domainName = '{{ domain_name }}';
    var s = domainName + "/embedded/page/popup/index.html",
        d = buildURL(s, {
            customer: escape(customer.customer),
            from: escape(customer.from),
            booked: escape(customer.booked),
            when: escape(customer.when)
        }),
        c = document.createElement("iframe");

    // delete all iframe
    var iframes = document.querySelectorAll('iframe');
	for (var i = 0; i < iframes.length; i++) {
		iframes[i].parentNode.removeChild(iframes[i]);
	}
    window.syncFrame = c, c.id = "box", c.frameBorder = 0, c.style.display = "none", c.src = d;
    var e = document.getElementsByTagName("script"),
        n = e.length - 1,
        u = e[n];

    u.parentNode.insertBefore(c, u);
    document.getElementById("box").classList.add("show");
}

function hideBox(){
    document.getElementById("box").classList.remove("show");
    document.getElementById("box").classList.add("hide");
}
function setup() {
    var domainName = '{{ domain_name }}';
    var client_id = '{{ client_id }}';
    var a = document.createElement("link");
    var assetPath = "{% static 'popup_embedder.css' %}";
    if(!assetPath.startsWith('https:')){
    	assetPath = domainName + assetPath;
		}
    a.rel = "stylesheet", a.type = "text/css", a.media = "all",a.href = assetPath;
    document.getElementsByTagName("head")[0].appendChild(a);
   
    getJSON(domainName + '/embedded/json/popup/' + client_id,
	function(err, data) {
	  if (err !== null) {
	    //do nothing
	  } else {
	  	var domainName = '{{ domain_name }}';

	  	var length = Object.keys(data).length;
	  	if (length){

	  		var s = domainName + "/embedded/page/popup/index.html",
			d = buildURL(s, {
				customer: escape(data[1].customer),
            	from: escape(data[1].from),
            	booked: escape(data[1].booked),
            	when: escape(data[1].when)
			}),
			c = document.createElement("iframe");
		    window.syncFrame = c, c.id = "box", c.frameBorder = 0, c.style.display = "none", c.src = d;
		    var e = document.getElementsByTagName("script"),
		        n = e.length - 1,
		        u = e[n];

		    u.parentNode.insertBefore(c, u);
		    document.getElementById("box").classList.add("show");
		    // if (length > 1){
			var data_keys = Object.keys(data);
			var interval_index = 0;

			var interval = setInterval(function(x,y) {
				if (document.getElementById("box").classList.contains("show")){
					hideBox();
					return
				}

				interval_index++;
				showBox(data[interval_index]);

				if (interval_index >= data_keys.length) {
					interval_index = 0;
					getJSON(domainName + '/embedded/json/popup/' + client_id,
					function(err, data) {
						data_keys = Object.keys(data);
					});
				}

			}, 6000);

		  	// } else {
		  	// 	setTimeout(function(){
			  // 		if (document.getElementById("box").classList.contains("show")){
			  //           hideBox();
			  //       }
              //
			  // 	}, 6000);
		  	// }
	    }
		
	  }
	});
    
}

! function() {
    setup()
}(this);