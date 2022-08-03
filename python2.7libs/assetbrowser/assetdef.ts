type AssetDef = {
    _schemaVersion: number,
    id: string, // asset unit id for tracking issues,
    author: string,
    description: string,
    createdOn: number,
    updatedOn: number,
    content: string // file path, vex snippet, ramp etc
};

type Asset = {
    _schemaVersion: number,
    id: string, // autogen uuid
    title: string,
    tags: string[],
    assetType: string,
    resolves: {
        // major.minor version
        [version: string]: string // path pointing to asset def 
    }
}