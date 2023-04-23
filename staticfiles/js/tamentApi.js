
const tamentApi = {
	lists : {
		getAll : function() {
			let url = "/lists/api/lists/"
			return commonApi.get({ url })
		},
		
		getOne : function(id) {
			let url = `/lists/api/lists/${id}/`
			return commonApi.get({ url })
		},
		
		create : function(data) {
			return commonApi.post({
				url : "/lists/api/lists/",
				body : data
			})
		},
		
		update : function(id,data) {
			return commonApi.put({
				url : `/lists/api/lists/${id}/`,
				body : data
			})
		},
		
		deleteOne : function(id) {
			let url = `/lists/api/lists/${id}/`
			return commonApi.deleteReq({ url })
		},
	},
	
	tasks : {
		getAll : function() {
			let url = "/lists/api/tasks/"
			return commonApi.get({ url })
		},
		
		getOne : function(id) {
			let url = `/lists/api/tasks/${id}/`
			return commonApi.get({ url })
		},
		
		add : function(data) {
			return commonApi.post({
				url : "/lists/api/tasks/",
				body : data
			})
		},
		
		updateOne : function(id,data) {
			return commonApi.patch({
				url : `/lists/api/tasks/${id}/`,
				body : data
			})	
		},
		
		toggleComplete : function(id,iscomplete) {
			return tamentApi.tasks.updateOne(id,{ complete : !iscomplete })
		},
		
		addSubtask : (id,payload) => tamentApi.tasks.add({
			...payload,
			subtask : true,
			task : id, 
		})
		
	}	
}