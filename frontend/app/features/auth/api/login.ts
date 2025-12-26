import { apiClient } from "~/shared/api/client";

export const loginFn = async (data: any) => (await apiClient.post("/auth/login", data)).data;
