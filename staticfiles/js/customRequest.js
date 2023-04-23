
var commonApi = "shsh"

commonApi = {
		__data_request : function(method,credentials) {
			let request = $.ajax({
				url : credentials.url,
				method : method,
				headers : { 
					'X-CSRFToken': csrftoken
				},
				data : credentials.body ?? {}, 
				...credentials.extra
			})
			return request
		},
		
		post : function(credentials) {
			return commonApi.__data_request("POST",credentials)
		},
		
		put : function(credentials) {
			return commonApi.__data_request("PUT",credentials)
		},
		
		patch : function(credentials) {
			return commonApi.__data_request("PATCH",credentials)
		},
		 
		
		deleteReq : function(credentials) {
			return commonApi.__data_request("DELETE",credentials)
		},
		
		upload : function(url,file) {	
			let request = commonApi.post({
				url : url,
				body : file,
				extra : {
					contentType : false,
					processData : false,
				}
			})
			return request
		},
		
		get : function(credentials) {
			let request = $.ajax({
				url : credentials.url,
				method : "GET",
				data : credentials.body ?? {}, 
				...credentials.extra
			})
			return request
		},
		
}

/*

const request = axios.create({
	baseUrl : "http://localhost:4000/"
})

request.defaults.headers.common["X-CSRFToken"] = csrftoken

//request.defaults.headers.common["Authentication"] = `Token ${token}`

*/








