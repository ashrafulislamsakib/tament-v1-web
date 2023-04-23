
import axios from 'axios';

class CrudApi {
	constructor(c) {
		this.config = c
		this.baseURL = this.config.baseURL ?? ''
		this.baseApiUrl = this.config.baseApiUrl ?? this.baseURL + 'api/'
		
		this.request = axios.create({
			baseURL,
		})
		
		if(this.config.authType = "token") {
			this.request.defaults.headers.common['Authorization'] = this.config.token
		}
		
		this.__createCrudUrl = id => {
			let url = `${this.baseApiUrl}${id}/`
			return url;
		}
	}
		
	getAll(url = this.baseApiUrl) {
		return this.request.get(url)
	}
	
	getOne(id) {
		let url = this.__createCrudUrl(id)
		return this.request.get(url)
		
	}
	
	add(data={},url = this.baseApiUrl) {
		return this.request.post(url,data)
	}
	
	updateOne(id,updatedData) {
		let url = this.__createCrudUrl(id)
		return this.request.patch(url,updatedData)
	}
	
	deleteOne(id) {
		let url = this.__createCrudUrl(id)
		return this.request.delete(url)
	}
	
}


const crudApi = {
	makeCrudAPI : config => {
		return new CrudApi(config)
	}
}

/*

import crudApi from 'crudApi'

const taskCrudApi = crudApi.makeCrudAPI({
	baseApiURL : "http://localhost:4000/lists/api/tasks/",
	authType : "token",
	token : `Token ${store.token}`
})

export default taskCrudApi


*/