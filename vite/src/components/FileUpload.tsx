export const FileUpload = () => {
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    const form = event.target as HTMLFormElement;
    const url = form.action;
    const input = form.elements[0] as HTMLInputElement;

    if (!input.files) {
      return;
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    const resp = await fetch(url, {
      method: "POST",
      body: formData,
    });

    console.log(resp);
  };

  return (
    <form
      action="/upload"
      onSubmit={handleSubmit}
      method="POST"
      encType="multipart/form-data"
    >
      <input type="file" className="file-input w-full max-w-xs" />

      <button className="btn btn-primary">Primary</button>
    </form>
  );
};
