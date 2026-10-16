export default function Home() {
  return (
    <main className="flex min-h-screen flex-col justify-between px-8 py-10 sm:px-16 sm:py-14">
      <header className="text-xl font-semibold tracking-tight">uragent</header>
      <section className="my-20 max-w-2xl">
        <p className="mb-5 text-sm font-medium text-zinc-500">A fresh start</p>
        <h1 className="text-5xl font-semibold tracking-tight sm:text-7xl">
          Ready for what&apos;s next.
        </h1>
        <p className="mt-7 max-w-lg text-lg leading-8 text-zinc-500">
          Your application is up and running. Built with Next.js, ready to make
          your own.
        </p>
        <a
          href="https://github.com/abhishyantkhare/uragent"
          className="mt-9 inline-flex rounded-full bg-foreground px-6 py-3 text-sm font-medium text-background transition-opacity hover:opacity-75"
        >
          View source
        </a>
      </section>
      <footer className="text-sm text-zinc-500">uragent &middot; Next.js</footer>
    </main>
  );
}
