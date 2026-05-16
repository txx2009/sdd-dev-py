import request from './request';

export const login = (data) => request.post('/v1/auth', data);
export const logout = () => request.delete('/v1/auth');
export const getMe = () => request.get('/v1/auth/me');