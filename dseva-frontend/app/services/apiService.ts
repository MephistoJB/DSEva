const apiService = {
    get: async function (url: string): Promise<any> {
        console.log('get', url)
        return new Promise((resolve, reject) => {
            fetch(`${process.env.NEXT_PUBLIC_API_HOST}${url}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then((json) => {
                console.log('Response:',json);

                resolve(json);
            })
            .catch((error) => {
                console.log('Error:',error);
            });
        })
            
    },

    post: async function (url: string, data: any): Promise<any> {
        console.log('post', url)
        return new Promise((resolve, reject) => {
            fetch(`${process.env.NEXT_PUBLIC_API_HOST}${url}`, {
                method: 'POST',
                body: data,
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then((json) => {
                console.log('Response:',json);

                resolve(json);
            })
            .catch((error) => {
                console.log('Error:',error);
            });
        })
            
    }
}

export default apiService;