import request from '../utils/request';

export const fetchData = (query) => {
    return request({
        url: '/api/video',
        method: 'get',
        params: query
    })
}
