import { listSubscriptions } from "@/api/subscriptions";
import { ThemeToggler } from "@/components/layout/theme-toggler";
import { CookieDropdown } from "@/features/cookies/cookie-dropdown";
import { useCookies } from "@/features/cookies/use-cookies";
import { useJobs } from "@/features/jobs/jobs-context";
import { useVersionCheck } from "@/hooks/use-version-check";
import {
  Button,
  buttonVariants,
  Chip,
  cn,
  Link as HeroUILink,
} from "@heroui/react";
import { Link, useRouterState } from "@tanstack/react-router";
import {
  Disc3Icon,
  DownloadIcon,
  ListMusicIcon,
  MenuIcon,
  RocketIcon,
  SettingsIcon,
  StarIcon,
  XIcon,
} from "lucide-react";
import { useEffect, useState } from "react";

const navItems = [
  { label: "Downloads", startIcon: DownloadIcon, href: "/" },
  { label: "My playlists", startIcon: ListMusicIcon, href: "/playlists" },
  { label: "Settings", startIcon: SettingsIcon, href: "/settings" },
];

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [subscriptionCount, setSubscriptionCount] = useState(0);
  const routerState = useRouterState();
  const currentPath = routerState.location.pathname;
  const {
    cookiesConfigured,
    isUploading,
    isDeleting,
    fileInputRef,
    handleFileSelect,
    handleDropdownAction,
    triggerFileUpload,
  } = useCookies();
  const { data: versionInfo } = useVersionCheck();
  const { hasActiveJobs } = useJobs();

  useEffect(() => {
    listSubscriptions().then((subs) => setSubscriptionCount(subs.length));
  }, []);

  // While the overlay menu is open, block page scroll and allow Escape to close
  // it (v2's Navbar did both for us).
  useEffect(() => {
    if (!isMenuOpen) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsMenuOpen(false);
    };
    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isMenuOpen]);

  return (
    <>
      <nav className="border-separator bg-background/70 sticky top-0 z-40 w-full border-b backdrop-blur-lg">
        <header className="mx-auto flex h-16 max-w-5xl items-center gap-2 px-4">
          {/* Mobile menu toggle */}
          <Button
            isIconOnly
            size="sm"
            variant="ghost"
            className="sm:hidden"
            aria-label={isMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={isMenuOpen}
            onPress={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <XIcon className="h-5 w-5" />
            ) : (
              <MenuIcon className="h-5 w-5" />
            )}
          </Button>

          {/* Brand */}
          <Link to="/" className="mr-4 flex items-center">
            <Disc3Icon
              className={`text-accent h-7 w-7 ${hasActiveJobs ? "animate-[spin_4s_linear_infinite] motion-reduce:animate-none" : ""}`}
            />
            <p className="text-foreground ml-2 text-xl font-bold">yubal</p>
          </Link>

          {/* Desktop navigation */}
          <ul className="hidden items-center gap-2 sm:flex">
            {navItems.map((item) => {
              const isActive = currentPath === item.href;
              return (
                <li key={item.href}>
                  <Link
                    to={item.href}
                    data-active={isActive || undefined}
                    className="text-muted data-[active]:text-foreground inline-flex items-center gap-2 rounded-lg px-3 py-1.5 text-sm font-medium hover:opacity-80"
                  >
                    <item.startIcon className="h-4 w-4" />
                    {item.label}
                    {item.href === "/playlists" && subscriptionCount > 0 && (
                      <Chip size="sm" variant="soft" className="font-mono">
                        {subscriptionCount}
                      </Chip>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>

          {/* Actions */}
          <div className="ml-auto flex items-center gap-2">
            {versionInfo?.updateAvailable && (
              <a
                href={versionInfo.releaseUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={cn(
                  buttonVariants({ size: "sm", variant: "ghost" }),
                  "hidden font-mono text-sm text-green-600 sm:inline-flex dark:text-green-400",
                )}
              >
                <RocketIcon className="h-4 w-4" />
                {versionInfo.latestVersion}
              </a>
            )}
            <a
              href="https://github.com/guillevc/yubal"
              target="_blank"
              rel="noopener noreferrer"
              className={cn(
                buttonVariants({ size: "sm", variant: "ghost" }),
                "hidden text-sm sm:inline-flex",
              )}
            >
              <StarIcon
                className="h-4 w-4 fill-amber-400 text-amber-400 dark:fill-amber-300 dark:text-amber-300"
                strokeWidth={1}
              />
              Star on GitHub
            </a>
            <div className="hidden sm:block">
              <CookieDropdown
                variant="desktop"
                cookiesConfigured={cookiesConfigured}
                isUploading={isUploading}
                isDeleting={isDeleting}
                onDropdownAction={handleDropdownAction}
                onUploadClick={triggerFileUpload}
              />
            </div>
            <ThemeToggler />
          </div>
        </header>

        {/* Hidden file input for cookie upload */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt"
          onChange={handleFileSelect}
          className="hidden"
        />
      </nav>

      {/* Mobile menu: overlays the page instead of pushing it down, so the
          sticky bar keeps its height and content below never shifts. Must live
          outside <nav>, whose backdrop-filter would otherwise make it the
          containing block for this fixed element. */}
      {isMenuOpen && (
        <div className="border-separator bg-background/90 fixed inset-x-0 top-16 bottom-0 z-30 overflow-y-auto border-t backdrop-blur-lg sm:hidden">
          <ul className="flex flex-col gap-4 p-6">
            {navItems.map((item) => (
              <li key={item.href}>
                <Link
                  to={item.href}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex w-full items-center gap-2 text-lg ${currentPath === item.href ? "text-accent" : "text-foreground"}`}
                >
                  {item.label}
                  {item.href === "/playlists" && subscriptionCount > 0 && (
                    <Chip size="sm" variant="soft" color="accent">
                      {subscriptionCount}
                    </Chip>
                  )}
                </Link>
              </li>
            ))}
            <li>
              <CookieDropdown
                variant="mobile"
                cookiesConfigured={cookiesConfigured}
                isUploading={isUploading}
                isDeleting={isDeleting}
                onDropdownAction={handleDropdownAction}
                onUploadClick={triggerFileUpload}
              />
            </li>
            <li>
              <HeroUILink
                href="https://github.com/guillevc/yubal"
                target="_blank"
                rel="noopener noreferrer"
                className="text-foreground w-full text-lg"
              >
                Star on GitHub
                <HeroUILink.Icon />
              </HeroUILink>
            </li>
          </ul>
        </div>
      )}
    </>
  );
}
