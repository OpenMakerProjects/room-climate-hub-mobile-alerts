"""MQTT telemetry to a configured ntfy topic; credentials only from environment."""
import json, math, os, time, urllib.request, urllib.parse

class Bridge:
    def __init__(self, base, topic, cooldown=300, sender=None, clock=time.monotonic):
        parsed=urllib.parse.urlparse(base)
        if parsed.scheme not in ('https','http') or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
            raise ValueError('Configure a dedicated ntfy server URL')
        if not topic or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in topic):
            raise ValueError('Invalid topic')
        self.url=base.rstrip('/')+'/'+topic;self.cooldown=cooldown;self.sender=sender or self.send;self.clock=clock
        self.last=None;self.active=False
    def send(self, message):
        headers={'Title':'Room climate alert','Content-Type':'text/plain; charset=utf-8'}
        if os.getenv('NTFY_TOKEN'):headers['Authorization']='Bearer '+os.environ['NTFY_TOKEN']
        req=urllib.request.Request(self.url,data=message.encode(),headers=headers,method='POST')
        with urllib.request.urlopen(req,timeout=10) as response:
            if response.status not in (200,201,202):raise RuntimeError('Notification rejected')
    def process(self, raw):
        record=json.loads(raw)
        if record.get('project_id')!=2 or record.get('valid') is not True:return False
        t=record.get('temperature_c');h=record.get('humidity_pct');p=record.get('pressure_hpa')
        if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in (t,h,p)):return False
        if not(-40<=t<=85 and 0<=h<=100 and 300<=p<=1100):return False
        if record.get('alert') is not True:self.active=False;return False
        now=self.clock()
        if self.active and self.last is not None and now-self.last<self.cooldown:return False
        self.sender(f'High temperature: {t:.2f} C; humidity {h:.2f}%; pressure {p:.2f} hPa')
        self.active=True;self.last=now;return True

def main():
    import paho.mqtt.client as mqtt
    bridge=Bridge(os.environ['NTFY_URL'],os.environ['NTFY_TOPIC'])
    client=mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id='omp-climate-002-mobile')
    if os.getenv('MQTT_USER'):client.username_pw_set(os.environ['MQTT_USER'],os.getenv('MQTT_PASSWORD'))
    if os.getenv('MQTT_TLS')=='1':client.tls_set()
    def connected(c,u,f,rc,properties):
        if rc==0:c.subscribe('openmaker/2/telemetry',qos=0)
    def received(c,u,message):
        try:bridge.process(message.payload.decode('utf-8'))
        except (ValueError,KeyError,UnicodeError):print('Rejected malformed telemetry',flush=True)
        except Exception:print('Notification delivery failed; next sample will retry',flush=True)
    client.on_connect=connected;client.on_message=received
    client.connect(os.environ['MQTT_HOST'],int(os.getenv('MQTT_PORT','1883')),60)
    client.loop_forever()
if __name__=='__main__':main()
