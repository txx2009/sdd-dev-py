import request from './request';

export const listUsers = (params) => request.get('/v1/users', { params });
export const getUser = (id) => request.get(`/v1/users/${id}`);
export const createUser = (data) => request.post('/v1/users', data);
export const updateUser = (id, data) => request.put(`/v1/users/${id}`, data);
export const deleteUser = (id) => request.delete(`/v1/users/${id}`);
export const changePassword = (id, data) => request.put(`/v1/users/${id}/password`, data);