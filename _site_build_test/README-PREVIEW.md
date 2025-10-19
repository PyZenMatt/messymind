PR Preview feature

This repository contains a GitHub Actions workflow that builds a PR preview of the Jekyll site and publishes it under the `gh-pages` branch to a subfolder per PR.

Preview URL pattern

- Each PR build publishes the static site to:
  `https://<owner>.github.io/<repo>/previews/pr-<PR_NUMBER>/`

What is included in the preview

- Jekyll is built with `--drafts` and `--future` enabled so drafts and posts with future dates are included.
- The build uses the repository `_config.yml` and the generated site is copied into `previews/pr-<PR_NUMBER>/` on the `gh-pages` branch.

Permissions required

- The workflow requires the repository Actions token to have `contents: write` and `issues: write` (and `pull-requests: write` if desired) so it can push to `gh-pages` and comment on the PR.
- To enable:
  1. Go to your repository on GitHub -> Settings -> Actions -> General.
  2. Under "Workflow permissions" choose "Read and write permissions".
  3. If using organization repo-level policies, ensure the org allows workflows to write to repository contents.

Pages configuration

- Ensure GitHub Pages is configured to serve from the `gh-pages` branch and the root folder. Go to Settings -> Pages and set "Branch: gh-pages" and "Folder: / (root)".


Testing the preview

1. Open a pull request that modifies a draft post or any content.
2. The `PR Preview` workflow will run and, if successful, push the built site to `gh-pages` under `previews/pr-<PR_NUMBER>/`.
3. The workflow will post a comment on the PR with the preview URL. It will update the same comment on subsequent commits.

Notes and troubleshooting

- If Pages is not configured to serve from `gh-pages` (root), the preview URL will not be served. Ensure Pages is set to the `gh-pages` branch and the root folder.
- If assets appear broken, ensure your templates use `relative_url` / `absolute_url` and rely on `site.baseurl` so that the site works from a subfolder. Typical fixes:
  - Use `{{ "/path" | relative_url }}` for links and assets.
  - Use `{{ site.baseurl }}` for absolute references inside the built HTML.
- The workflow modifies `published: false` to `published: true` in the repo copy used for the preview build; this is only for the built artifact pushed to `gh-pages`.
- The preview uses `--drafts` and `--future`, so drafts and posts with future dates will appear.

If you need help enabling repository permissions or testing, ping the maintainers.

--
Generated: PR Preview workflow