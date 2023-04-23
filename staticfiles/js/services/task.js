

let baseUrl = "/lists/api/tasks/"

const TaskApi = {
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
	
	updateOne : (id,payload) => {
		return request.patch(`${baseUrl}${id}/`,payload)
	},
	
	toggleComplete : id => {
		return TaskApi.getOne(id).then(data => {
			if(!data) return
			return TaskApi.updateOne(id,{ complete : !data.complete })
		})
	},
	
	addSubtask : (id,payload) => {
		return TaskApi.add({
			parent : id,
			subtask : true,
			...payload
		})
	}
	
	
	
	//mark all as complete
	
	deleteOne : id => request.delete(`/lists/api/tasks/${id}/`)
}

export default TaskApi

