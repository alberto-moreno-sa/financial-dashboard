import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { apiClient } from "~/shared/api/client";

export function useUploadPortfolio() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      return (await apiClient.post("/portfolio/upload", formData)).data;
    },
    onMutate: () => toast.loading("Processing portfolio..."),
    onSuccess: () => {
      toast.dismiss();
      toast.success("Portfolio synced");
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
      queryClient.invalidateQueries({ queryKey: ["holdings"] });
      queryClient.invalidateQueries({ queryKey: ["history"] });
    },
    onError: () => {
      toast.dismiss();
      toast.error("Upload failed");
    },
  });
}
