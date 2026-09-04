import { Chip, tv, type VariantProps } from "@heroui/react";
import { ReactNode } from "react";

const jobChip = tv({
  base: "font-mono",
  variants: {
    variant: {
      // `--default-soft` sits within ~1% lightness of the row's surface, so the
      // neutral chips need their own contrast against the card background.
      flat: "bg-foreground/10 text-muted",
      album: "bg-accent/15 text-accent",
      playlist: "bg-secondary/15 text-secondary",
      track:
        "bg-amber-500/15 text-amber-600 dark:bg-amber-500/20 dark:text-amber-300",
      podcast_episode:
        "bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-300",
    },
  },
  defaultVariants: {
    variant: "flat",
  },
});

type Props = {
  children: ReactNode;
  className?: string;
} & VariantProps<typeof jobChip>;

export function JobChip({ children, variant, className }: Props) {
  return (
    // `md` keeps the base chip padding (px-2 py-0.5); `sm` squashes it to px-1 py-0.
    <Chip size="md" variant="soft" className={jobChip({ variant, className })}>
      {children}
    </Chip>
  );
}
