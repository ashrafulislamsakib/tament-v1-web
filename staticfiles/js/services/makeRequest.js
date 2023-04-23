let baseurl = 'http://localhost:4000/'

class MakeRequest {
	contractor(data={}) {
		this.data = data
		this.baseURL = this.data.baseURL ?? ''
		
		this.defaults = {
			headers : {
				"Content-Type" : "application/json",
			}
		}
		
		//this.authType = data?.authType = "jwt"
		
	}
	
	config(data) { 
		this.data = data
		return this
	}
	
	__create_request(path,options) {
		let url = this.baseURL + path
		if(url.startsWith("http://") || url.startsWith("https://")) {
			url = path
		}
		let def = this.defaults
		let formatedOptions = {
			...def,
			...options,
		}
		
		
		return fetch(url,formatedOptions).then(res => {
			return {
				body : res.json(),
				status: res.status,
			}
		})
	}
	
	__request(path,method,payload) {
		return this.__create__request(path,{
			method : method,
			body : payload
		})
	}
	
	post(path,payload={}) {
		return this.__request(path,"POST",payload);
	}
	
	
	patch(path,payload={}) {
		return this.__create__request(path,{
			method : "PATCH",
			body : payload
		})
	}
	
	
	put(path,payload={}) {
		return this.__create__request(path,{
			method : "PUT",
			body : payload
		})
	}
	
	
	delete(path,payload={}) {
		return this.__create__request(path,{
			method : "DELETE",
			body : payload
		})
	}
	
	
}


const request = new MakeRequest()

//request.defaults.headers["Autherization"] = "Bearer " + String(getState().auth?.token?.access)



export default request
