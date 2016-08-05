export function getMetadataTitle(metadata) {
  let rv = metadata.label;
  if (metadata.status) {
    rv += ' ' + metadata.status;
  }
  return rv;
}

export function getMetadataSubtitle(metadata) {
  let rv = metadata.executable;
  if (metadata.exit_code !== null) {
    rv += ' exited with ' + metadata.exit_code;
  }
  return rv;
}
