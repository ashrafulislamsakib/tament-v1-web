
let baseUrl = "/lists/api/lists/"

const ListApi = {
	getAll : () => { 
		return request.get(baseUrl).then(res => res.data)
	},
	
	getOne : id => {
		return request.get(`${baseUrl}${id}/`).then(res => res.data)
	},
	
	add : payload => {
		return request
			.post(baseUrl,payload)
			.then(res => res.data)
	},
	
	updateName : (id,payload) => {
		return request.patch(`${baseUrl}${id}/`,payload)
	},
	
	//mark all as complete
	
	deleteOne : (id) => request.delete(`${baseUrl}${id}/`)
}

export default ListApi

