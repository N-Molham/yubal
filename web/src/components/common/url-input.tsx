import { isValidUrl } from "@/lib/url";
import { CloseButton, FieldError, InputGroup, TextField } from "@heroui/react";
import { LinkIcon } from "lucide-react";

type Props = {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
  placeholder?: string;
};

export function UrlInput({
  value,
  onChange,
  disabled,
  placeholder = "Album or playlist URL",
}: Props) {
  const isValid = value === "" || isValidUrl(value);

  return (
    <TextField
      type="url"
      value={value}
      onChange={(v) => onChange(v.trim())}
      isDisabled={disabled}
      isInvalid={!isValid}
      fullWidth
      aria-label={placeholder}
    >
      <InputGroup className="min-w-0">
        <InputGroup.Prefix>
          <LinkIcon className="text-muted h-4 w-4" />
        </InputGroup.Prefix>
        {/* The bare input keeps its intrinsic ~20ch width and would push the
            row past the viewport on narrow screens without min-w-0. */}
        <InputGroup.Input
          className="w-full min-w-0"
          placeholder={placeholder}
        />
        {value !== "" && (
          <InputGroup.Suffix>
            <CloseButton aria-label="Clear" onPress={() => onChange("")} />
          </InputGroup.Suffix>
        )}
      </InputGroup>
      {!isValid && <FieldError>Enter a valid URL</FieldError>}
    </TextField>
  );
}
