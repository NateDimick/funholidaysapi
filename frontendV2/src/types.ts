export type NavItemProp = {
    link: string,
    mainText: string,
    linkText: string
}

export class QueryParams {

    private queryMap: object = {}

    static from(qs:string): QueryParams {
        let qp = new QueryParams()
        let pairs = qs.split("&")
        pairs.forEach(p => {
            let kv = p.split("=")
            qp.set(decodeURIComponent(kv[0]), decodeURIComponent(kv[1]))
        })
        return qp
    }

    public has(key:string): boolean {
        if (this.get(key)) {
            return true
        } else {
            return false
        }
    }

    public get(key:string): string {
        return this.queryMap[key]
    }

    private set(key:string, value:string) {
        this.queryMap[key] = value
    }    
}