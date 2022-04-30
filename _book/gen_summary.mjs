import { opendir } from 'fs/promises';

try {
  console.log("* [Introduction](README.md)");
  const dir = await opendir('./');
  for await (const dirent of dir)
    if (dirent.isDirectory() && !dirent.name.startsWith('.') && !dirent.name.startsWith('_')  && dirent.name!='node_modules') {
      console.log("* " + dirent.name);
      const subDir = await opendir(dirent.name);
      for await (const f of subDir)
        if(f.isFile()){
          console.log("  * [" + f.name.slice(0,-3)+"]("+dirent.name+"/"+f.name+")");
        }
    }
} catch (err) {
  console.error(err);
}