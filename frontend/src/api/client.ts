/** 统一请求封装：拼后端地址、抛网络错误、给页脚留一句可读的说明。 */
const API_BASE = import.meta.env.VITE_API_BASE ?? ''

export function request(path: string, init?: RequestInit): Promise<Response> {
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`
  return fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  }).catch((error: unknown) => {
    const detail = error instanceof Error ? error.message : '请求未送达'
    throw new Error(`接口请求失败：${detail}`)
  })
}

export async function fetchJson<T>(path: string): Promise<T> {
  const response = await request(path)
  if (!response.ok) {
    throw new Error(`接口返回 ${response.status}，数据未更新`)
  }
  return (await response.json()) as T
}

/** 列表回包：字段名与后端 PageResult 对齐（items/total/page/size）。 */
export type PagePayload<Row> = {
  items: Row[]
  total: number
  page: number
  size: number
}

/** 动作回包：字段名与后端 ActionResult 对齐（ok/message/entry）。 */
export type ActionPayload = {
  ok: boolean
  message: string
  entry?: Record<string, unknown> | null
}

/** 错误回包统一读 message：HTTP 层错误与业务失败都是这一个字段。 */
async function readError(response: Response, fallback: string): Promise<Error> {
  try {
    const payload = (await response.json()) as { message?: unknown }
    if (typeof payload.message === 'string' && payload.message) {
      return new Error(payload.message)
    }
  } catch {
    // 回包不是 JSON 时落到默认说明
  }
  return new Error(fallback)
}

/** 读列表：各模块页面共用，不再每个页面各解析一遍。 */
export async function fetchPage<Row>(path: string): Promise<PagePayload<Row>> {
  const response = await request(path)
  if (!response.ok) {
    throw await readError(response, `接口返回 ${response.status}，列表读取失败`)
  }
  const payload = (await response.json()) as Partial<PagePayload<Row>>
  const items = payload.items ?? []
  return {
    items,
    total: payload.total ?? items.length,
    page: payload.page ?? 1,
    size: payload.size ?? items.length,
  }
}

/** 执行动作：ok 为 false 时以后端 message 为错误说明，与后端口径一致。 */
export async function postAction(path: string, body: unknown): Promise<ActionPayload> {
  const response = await request(path, {
    method: 'POST',
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    throw await readError(response, `接口返回 ${response.status}，动作未生效`)
  }
  const payload = (await response.json()) as ActionPayload
  if (!payload.ok) {
    throw new Error(payload.message || '动作未生效')
  }
  return payload
}
