import { Skeleton } from "~/shared/ui/skeleton";

export function DashboardSkeleton() {
  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar Skeleton */}
      <aside className="hidden w-64 flex-col border-r border-gray-200 bg-white md:flex">
        <div className="border-b border-gray-100 p-6">
          <Skeleton className="h-7 w-32" />
        </div>

        <nav className="flex-1 space-y-2 px-4 py-6">
          <Skeleton className="h-10 w-full rounded-md" />
        </nav>

        <div className="border-t border-gray-100 p-4">
          <Skeleton className="h-10 w-full rounded-md" />
        </div>
      </aside>

      {/* Main Content Skeleton */}
      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        {/* Mobile Header Skeleton */}
        <div className="flex items-center justify-between border-b border-gray-200 bg-white p-4 md:hidden">
          <Skeleton className="h-6 w-24" />
          <Skeleton className="h-8 w-16" />
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          <div className="space-y-8">
            {/* Header Skeleton */}
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <Skeleton className="h-8 w-48 mb-2" />
                <Skeleton className="h-4 w-96" />
              </div>
            </div>

            {/* Stats Cards Skeleton */}
            <section>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                    <div className="flex items-center justify-between">
                      <Skeleton className="h-4 w-20" />
                      <Skeleton className="h-5 w-5 rounded" />
                    </div>
                    <Skeleton className="mt-4 h-8 w-32" />
                    <Skeleton className="mt-2 h-4 w-16" />
                  </div>
                ))}
              </div>
            </section>

            {/* Holdings Table Skeleton */}
            <section className="grid gap-6 lg:grid-cols-1">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Skeleton className="h-6 w-40" />
                </div>

                <div className="rounded-lg border border-gray-200 bg-white shadow-sm">
                  <div className="border-b border-gray-200 p-6">
                    <div className="flex items-center justify-between">
                      <Skeleton className="h-6 w-36" />
                      <Skeleton className="h-6 w-20 rounded-full" />
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="space-y-3">
                      {[...Array(5)].map((_, i) => (
                        <div key={i} className="flex items-center gap-4">
                          <Skeleton className="h-12 w-20" />
                          <Skeleton className="h-12 flex-1" />
                          <Skeleton className="h-12 w-24" />
                          <Skeleton className="h-12 w-24" />
                          <Skeleton className="h-12 w-24" />
                          <Skeleton className="h-12 w-32" />
                          <Skeleton className="h-12 w-28" />
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
